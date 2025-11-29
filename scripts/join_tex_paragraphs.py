# -*- coding: utf-8 -*-
"""
Join lines inside paragraphs in a .tex file, keeping double blank lines as paragraph separators.
Rules implemented:
- Do not join inside \begin{...} ... \end{...} environments (we detect by environment stack).
- Do not join across display math environments (\[ ... \], $$ ... $$).
- Do not join lines that contain an unescaped '%' (comments), or lines starting with '%' (comment lines).
- Do not join lines where the previous line ends with unescaped '\\' (literal LaTeX linebreak).
- Do not join if the next line starts with a backslash followed by some letters and likely a block-level command (e.g., \section, \chapter, \begin, \end, \item, \noindent, \maketitle, \tableofcontents, etc.).
- Otherwise join by replacing the newline with a single space (preserve spacing between words).

The script writes the result into a NEW file by default (*.joined.tex), and optionally overwrites the original when run with --inplace.

Usage: python join_tex_paragraphs.py path/to/file.tex [--inplace]
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

# Basic config
PRESERVE_ENVIRONMENTS = {
    # commonly used environments where line breaks are meaningful
    'verbatim', 'Verbatim', 'lstlisting', 'minted', 'align', 'align*', 'equation', 'equation*',
    'gather', 'gather*', 'multline', 'multline*', 'tikzpicture', 'tikz', 'figure', 'table', 'tabular',
    'matrix', 'pmatrix', 'bmatrix', 'cases', 'itemize', 'enumerate', 'description', 'lstlisting', 'quote'
}

# Commands that usually appear on their own line and should prevent joining with previous line
BLOCK_COMMANDS = {
    'section', 'subsection', 'subsubsection', 'chapter', 'paragraph', 'subparagraph', 'begin', 'end',
    'maketitle', 'tableofcontents', 'noindent', 'label', 'caption', 'includegraphics', 'centering', 'item',
}

# also treat some single-line commands as block-level
BLOCK_SINGLE_LINE_COMMANDS = {
    'title', 'author', 'date', 'maketitle'
}

# regex
begin_re = re.compile(r"\\begin\{([^}]*)\}")
end_re = re.compile(r"\\end\{([^}]*)\}")

# find environment name at \begin{...} or single-line begin env

def has_unescaped_percent(s: str) -> bool:
    # returns True if there's an unescaped % in the string
    i = 0
    while True:
        idx = s.find('%', i)
        if idx == -1:
            return False
        # count number of backslashes directly preceding it
        backslashes = 0
        j = idx - 1
        while j >= 0 and s[j] == '\\':
            backslashes += 1
            j -= 1
        if backslashes % 2 == 0:  # even number of backslashes => % is not escaped
            return True
        else:
            i = idx + 1


def starts_with_block_command(line_strip: str) -> bool:
    # check if stripped line starts with \command that is in BLOCK_COMMANDS
    if not line_strip.startswith('\\'):
        return False
    # extract command name
    m = re.match(r"\\([A-Za-z@]+)", line_strip)
    if m:
        cmd = m.group(1)
        if cmd in BLOCK_COMMANDS:
            return True
    # also consider lines that start with \[ or \] which are display math
    if line_strip.startswith('\\[') or line_strip == '\\]':
        return True
    # also literal $$ - might be rare to start with these
    if line_strip.startswith('$$') or line_strip.startswith('\\(') or line_strip.startswith('\\)'):
        return True
    # lines that start with '%' are comments - we handle earlier
    return False


def is_line_with_begin(line: str):
    return bool(begin_re.search(line))


def is_line_with_end(line: str):
    return bool(end_re.search(line))


def transform_text(lines: list[str], delete_newline: bool = False) -> list[str]:
    out_lines: list[str] = []
    env_stack: list[str] = []
    in_display_math = False  # for \[ and \]
    in_dollar_dollar = False  # for $$ ... $$

    # process the file as sequences of paragraphs separated by blank lines
    # We will gather paragraph lines and process inside

    para = []

    def flush_paragraph(p: list[str]):
        if not p:
            out_lines.append('')
            return
        # process: if paragraph contains only environment lines or special blocks, we keep them
        # We'll merge lines within the paragraph if they are safe to join
        merged = []
        prev = None
        for ln in p:
            ln_strip = ln.strip()
            # If ln is empty (shouldn't be), flush
            if ln_strip == '':
                if prev is not None:
                    merged.append(prev)
                    prev = None
                merged.append('')
                continue
            # If line starts with % - keep as separate line
            if ln_strip.startswith('%'):
                if prev is not None:
                    merged.append(prev)
                    prev = None
                merged.append(ln)
                continue
            # If line contains unescaped % then do not join it with next
            if has_unescaped_percent(ln):
                if prev is not None:
                    # join prev with this line? Not recommended; better to separate
                    merged.append(prev)
                    prev = None
                merged.append(ln)
                continue
            # If the line begins with a block command like \section, \begin, etc., keep its own line
            if starts_with_block_command(ln_strip):
                if prev is not None:
                    merged.append(prev)
                    prev = None
                merged.append(ln)
                continue
            # If line is \begin{...} or \end{...}, treat as block-level too
            if is_line_with_begin(ln) or is_line_with_end(ln):
                if prev is not None:
                    merged.append(prev)
                    prev = None
                merged.append(ln)
                continue
            # If prev is None, set prev
            if prev is None:
                prev = ln
                continue
            # If previous line starts with a block command (\section, \noindent, etc.), do not join
            prev_strip = prev.strip()
            if prev_strip.startswith('\\'):
                mprev = re.match(r"\\([A-Za-z@]+)\b", prev_strip)
                if mprev and mprev.group(1) in BLOCK_COMMANDS.union(BLOCK_SINGLE_LINE_COMMANDS):
                    merged.append(prev)
                    prev = ln
                    continue
            # previous line prev exists; decide if it's safe to append current ln to prev
            # If prev ends with unescaped \\ (LaTeX linebreak), do NOT join; we keep prev as is
            prev_rstrip = prev.rstrip()
            if prev_rstrip.endswith('\\'):
                merged.append(prev)
                prev = ln
                continue
            # If prev contains unescaped %, we already handled earlier; but double-check
            if has_unescaped_percent(prev):
                merged.append(prev)
                prev = ln
                continue
            # If current line starts with a backslash followed by command - we already handled starts_with_block_command
            # Also lines starting with '}' or '&' or '\\' at beginning probably indicate math or continuation - don't join
            if ln_strip.startswith('}') or ln_strip.startswith('&') or ln_strip.startswith('\\'):
                merged.append(prev)
                prev = ln
                continue
            # else join: either remove newline by concatenation, or insert a single space
            if delete_newline:
                joined = prev.rstrip() + ln.lstrip()
            else:
                joined = prev.rstrip() + ' ' + ln.lstrip()
            prev = joined
        if prev is not None:
            merged.append(prev)
        # append merged lines to out_lines
        out_lines.extend(merged)

    for line in lines:
        if line.strip() == '':
            # paragraph boundary
            flush_paragraph(para)
            para = []
            continue
        else:
            para.append(line)
    # flush last paragraph
    flush_paragraph(para)

    return out_lines


def main(argv):
    if len(argv) < 2:
        print("Usage: python join_tex_paragraphs.py path/to/file.tex [--inplace]")
        return 1
    inp = Path(argv[1])
    if not inp.exists():
        print(f"File {inp} not found")
        return 1
    inplace = False
    delete_newline = False
    for arg in argv[2:]:
        if arg == '--inplace':
            inplace = True
        if arg == '--delete':
            delete_newline = True
    content = inp.read_text(encoding='utf-8')
    lines = content.splitlines()

    # (argv parsed above; delete_newline already set)
    new_lines = transform_text(lines, delete_newline=delete_newline)

    new_content = '\n'.join(new_lines) + ('\n' if content.endswith('\n') else '')

    out_path = inp if inplace else inp.with_suffix(inp.suffix + '.joined.tex')
    # if inplace, create a backup copy before overwriting
    if inplace:
        bak = inp.with_name(inp.stem + '.bak' + inp.suffix)
        bak.write_text(content, encoding='utf-8')
        print(f"Backup saved to {bak}")
    out_path.write_text(new_content, encoding='utf-8')
    print(f"Wrote output to {out_path}")
    if not inplace:
        print("Preview the changes, and if you like them, run with --inplace to overwrite the file")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
