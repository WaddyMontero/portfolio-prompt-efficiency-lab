from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


PATCH_PATH_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.MULTILINE)

SEARCH_TOOLS = {"file_search", "grep_search", "list_dir"}
EDIT_TOOLS = {
    "apply_patch",
    "create_file",
    "replace_string_in_file",
    "multi_replace_string_in_file",
}
CONTINUATION_PROMPTS = {"proceed", "continue", "go on", "next"}

SCOPE_PATTERNS = {
    "portfolio_reporting": "models/gold/portfolio_reporting/",
    "silver": "models/silver/",
    "compliance": "models/gold/compliance/",
    "archived": "models/gold/archived/",
    "analyses": "analyses/",
    "docs": "docs/",
    "showcase": "showcase/",
    "scripts": "scripts/",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize AI coding-agent export logs into workshop scorecard metrics."
    )
    parser.add_argument("exports", nargs="+", help="Paths to exported JSON log files.")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_tool_args(log: dict) -> dict:
    raw_args = log.get("args")
    if not raw_args:
        return {}

    try:
        return json.loads(raw_args)
    except json.JSONDecodeError:
        return {}


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def path_scope(path: str) -> str | None:
    normalized = normalize_path(path)
    for label, needle in SCOPE_PATTERNS.items():
        if needle in normalized:
            return label
    if normalized.endswith("/AGENTS.md") or normalized.endswith("AGENTS.md"):
        return "agents"
    return None


def extract_edit_paths(log: dict) -> list[str]:
    tool = log.get("tool")
    args = parse_tool_args(log)

    if tool in {"create_file", "replace_string_in_file", "multi_replace_string_in_file"}:
        file_path = args.get("filePath")
        return [file_path] if isinstance(file_path, str) else []

    if tool == "apply_patch":
        patch = args.get("input", "")
        if not isinstance(patch, str):
            return []
        return PATCH_PATH_RE.findall(patch)

    return []


def collect_request_usage(logs: list[dict]) -> dict:
    usage = {
        "request_turns": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "cached_prompt_tokens": 0,
        "uncached_prompt_tokens": 0,
        "reasoning_tokens": 0,
        "duration_ms": 0,
        "ttfb_ms": 0,
    }

    for log in logs:
        if log.get("kind") != "request" or log.get("name") != "panel/editAgent":
            continue

        metadata = log.get("metadata") or {}
        usage_data = metadata.get("usage") or {}
        prompt_tokens = usage_data.get("prompt_tokens", 0) or 0
        cached_tokens = (usage_data.get("prompt_tokens_details") or {}).get("cached_tokens", 0) or 0

        usage["request_turns"] += 1
        usage["prompt_tokens"] += prompt_tokens
        usage["completion_tokens"] += usage_data.get("completion_tokens", 0) or 0
        usage["total_tokens"] += usage_data.get("total_tokens", 0) or 0
        usage["cached_prompt_tokens"] += cached_tokens
        usage["uncached_prompt_tokens"] += max(prompt_tokens - cached_tokens, 0)
        usage["reasoning_tokens"] += (
            (usage_data.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0
        )
        usage["duration_ms"] += metadata.get("duration", 0) or 0
        usage["ttfb_ms"] += metadata.get("timeToFirstToken", 0) or 0

    return usage


def summarize_prompt(prompt: dict) -> dict:
    reads: list[str] = []
    edits: list[str] = []
    commands: list[str] = []
    search_calls = 0
    tool_calls = 0
    scope_counter: Counter[str] = Counter()
    usage = collect_request_usage(prompt.get("logs", []))

    for log in prompt.get("logs", []):
        if log.get("kind") != "toolCall":
            continue

        tool_calls += 1
        tool = log.get("tool")
        args = parse_tool_args(log)

        if tool == "read_file":
            file_path = args.get("filePath")
            if isinstance(file_path, str):
                reads.append(file_path)
                scope = path_scope(file_path)
                if scope:
                    scope_counter[scope] += 1

        if tool in SEARCH_TOOLS:
            search_calls += 1
            search_path = args.get("path")
            if isinstance(search_path, str):
                scope = path_scope(search_path)
                if scope:
                    scope_counter[scope] += 1

        if tool == "run_in_terminal":
            command = args.get("command")
            if isinstance(command, str):
                commands.append(command)

        if tool in EDIT_TOOLS:
            for path in extract_edit_paths(log):
                edits.append(path)
                scope = path_scope(path)
                if scope:
                    scope_counter[scope] += 1

    validation_commands = [
        command
        for command in commands
        if "dbt build" in command or "dbt test" in command or "dbt seed" in command
    ]

    prompt_text = prompt.get("prompt", "").strip()
    prompt_slug = prompt_text.replace("\n", " ")

    return {
        "prompt": prompt_slug,
        **usage,
        "tool_calls": tool_calls,
        "search_calls": search_calls,
        "read_count": len(reads),
        "unique_reads": sorted(set(reads)),
        "edit_count": len(edits),
        "unique_edits": sorted(set(edits)),
        "commands": commands,
        "validation_commands": validation_commands,
        "scope_counter": scope_counter,
    }


def is_continuation_prompt(prompt_text: str) -> bool:
    return prompt_text.strip().lower() in CONTINUATION_PROMPTS


def merge_prompt_summaries(prompts: list[dict]) -> list[dict]:
    merged: list[dict] = []

    for prompt in prompts:
        if merged and is_continuation_prompt(prompt["prompt"]):
            previous = merged[-1]
            previous["prompt"] = f"{previous['prompt']} + {prompt['prompt']}"

            for key in [
                "request_turns",
                "prompt_tokens",
                "completion_tokens",
                "total_tokens",
                "cached_prompt_tokens",
                "uncached_prompt_tokens",
                "reasoning_tokens",
                "duration_ms",
                "ttfb_ms",
                "tool_calls",
                "search_calls",
                "read_count",
                "edit_count",
            ]:
                previous[key] += prompt[key]

            previous["unique_reads"] = sorted(set(previous["unique_reads"]) | set(prompt["unique_reads"]))
            previous["unique_edits"] = sorted(set(previous["unique_edits"]) | set(prompt["unique_edits"]))
            previous["commands"].extend(prompt["commands"])
            previous["validation_commands"].extend(prompt["validation_commands"])
            previous["scope_counter"].update(prompt["scope_counter"])
            continue

        merged.append(prompt)

    return merged


def summarize_export(path: Path) -> dict:
    data = load_json(path)
    raw_prompts = [
        summarize_prompt(prompt)
        for prompt in data.get("prompts", [])
        if prompt.get("prompt") != "title"
    ]
    prompts = merge_prompt_summaries(raw_prompts)

    total_scope_counter: Counter[str] = Counter()
    unique_reads: set[str] = set()
    unique_edits: set[str] = set()
    commands: list[str] = []

    for prompt in prompts:
        total_scope_counter.update(prompt["scope_counter"])
        unique_reads.update(prompt["unique_reads"])
        unique_edits.update(prompt["unique_edits"])
        commands.extend(prompt["commands"])

    validation_commands = [
        command
        for command in commands
        if "dbt build" in command or "dbt test" in command or "dbt seed" in command
    ]

    return {
        "path": path,
        "exported_at": data.get("exportedAt"),
        "total_prompts": len(prompts),
        "normalized_prompts": len(prompts),
        "raw_prompts": len(raw_prompts),
        "raw_total_prompts": data.get("totalPrompts", len(prompts)),
        "total_log_entries": data.get("totalLogEntries", 0),
        "request_turns": sum(prompt["request_turns"] for prompt in prompts),
        "prompt_tokens": sum(prompt["prompt_tokens"] for prompt in prompts),
        "completion_tokens": sum(prompt["completion_tokens"] for prompt in prompts),
        "total_tokens": sum(prompt["total_tokens"] for prompt in prompts),
        "cached_prompt_tokens": sum(prompt["cached_prompt_tokens"] for prompt in prompts),
        "uncached_prompt_tokens": sum(prompt["uncached_prompt_tokens"] for prompt in prompts),
        "reasoning_tokens": sum(prompt["reasoning_tokens"] for prompt in prompts),
        "duration_ms": sum(prompt["duration_ms"] for prompt in prompts),
        "ttfb_ms": sum(prompt["ttfb_ms"] for prompt in prompts),
        "tool_calls": sum(prompt["tool_calls"] for prompt in prompts),
        "search_calls": sum(prompt["search_calls"] for prompt in prompts),
        "read_count": sum(prompt["read_count"] for prompt in prompts),
        "unique_reads": sorted(unique_reads),
        "edit_count": sum(prompt["edit_count"] for prompt in prompts),
        "unique_edits": sorted(unique_edits),
        "commands": commands,
        "validation_commands": validation_commands,
        "scope_counter": total_scope_counter,
        "prompts": prompts,
    }


def short_prompt(prompt: str, width: int = 72) -> str:
    prompt = prompt.strip()
    if len(prompt) <= width:
        return prompt
    return f"{prompt[: width - 3]}..."


def print_scope_lines(scope_counter: Counter[str]) -> None:
    if not scope_counter:
        print("  scope touches: none classified")
        return

    ordered_labels = [
        "portfolio_reporting",
        "silver",
        "docs",
        "agents",
        "compliance",
        "archived",
        "analyses",
        "showcase",
        "scripts",
    ]
    parts = [f"{label}={scope_counter[label]}" for label in ordered_labels if scope_counter[label]]
    print(f"  scope touches: {', '.join(parts)}")


def print_summary(summary: dict) -> None:
    print(f"\n=== {summary['path'].name} ===")
    print(f"exportedAt: {summary['exported_at']}")
    print(
        "overall:"
        f" prompts={summary['normalized_prompts']} (raw={summary['raw_prompts']})"
        f" request_turns={summary['request_turns']}"
        f" prompt_tokens={summary['prompt_tokens']}"
        f" uncached_prompt_tokens={summary['uncached_prompt_tokens']}"
        f" completion_tokens={summary['completion_tokens']}"
        f" total_tokens={summary['total_tokens']}"
        f" tool_calls={summary['tool_calls']}"
        f" searches={summary['search_calls']}"
        f" reads={summary['read_count']} ({len(summary['unique_reads'])} unique)"
        f" edits={summary['edit_count']} ({len(summary['unique_edits'])} unique)"
        f" terminal_commands={len(summary['commands'])}"
        f" validation_commands={len(summary['validation_commands'])}"
    )
    print(
        "  timing:"
        f" duration_ms={summary['duration_ms']}"
        f" ttfb_ms={summary['ttfb_ms']}"
        f" cached_prompt_tokens={summary['cached_prompt_tokens']}"
        f" reasoning_tokens={summary['reasoning_tokens']}"
    )
    print_scope_lines(summary["scope_counter"])

    if summary["unique_edits"]:
        print("  edited files:")
        for path in summary["unique_edits"]:
            print(f"  - {path}")

    if summary["commands"]:
        print("  terminal commands:")
        for command in summary["commands"]:
            print(f"  - {command}")

    print("\n  per prompt:")
    for index, prompt in enumerate(summary["prompts"], start=1):
        print(
            f"  {index}. {short_prompt(prompt['prompt'])}\n"
            f"     turns={prompt['request_turns']} tool_calls={prompt['tool_calls']} "
            f"uncached_prompt_tokens={prompt['uncached_prompt_tokens']} "
            f"searches={prompt['search_calls']} reads={prompt['read_count']} "
            f"({len(prompt['unique_reads'])} unique) edits={prompt['edit_count']} "
            f"({len(prompt['unique_edits'])} unique) terminal={len(prompt['commands'])} "
            f"validation={len(prompt['validation_commands'])}"
        )
        print_scope_lines(prompt["scope_counter"])


def main() -> None:
    args = parse_args()
    for export in args.exports:
        print_summary(summarize_export(Path(export).expanduser().resolve()))


if __name__ == "__main__":
    main()
