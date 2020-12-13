from html import escape
from typing import List, Optional, cast

from mistune import AstRenderer, BlockParser, InlineParser, Markdown

from ..hooks import (
    convert_block_ast_to_rich_text_hook,
    convert_inline_ast_to_text_hook,
    create_markdown_hook,
)
from ..types import GraphQLContext, MarkdownPlugin, RichText, RichTextBlock
from ..utils.strings import get_random_string
from .markdown import html_markdown


async def parse_markup(context: GraphQLContext, markup: str) -> RichText:
    markdown = create_markdown(context)
    ast = markdown(markup)

    return convert_ast_to_richtext(context, ast)


def create_markdown(context: GraphQLContext) -> Markdown:
    return create_markdown_hook.call_action(
        create_markdown_action, context, BlockParser(), InlineParser(AstRenderer()), []
    )


def create_markdown_action(
    context: GraphQLContext,
    block: BlockParser,
    inline: InlineParser,
    plugins: List[MarkdownPlugin],
) -> Markdown:
    return Markdown(None, block, inline, plugins)


def convert_ast_to_richtext(context: GraphQLContext, ast: List[dict]) -> RichText:
    rich_text = []
    for node in ast:
        richtext_block = convert_block_ast_to_richtext(context, node)
        if richtext_block:
            rich_text.append(richtext_block)

    return cast(RichText, rich_text)


def convert_block_ast_to_richtext(
    context: GraphQLContext, ast: dict
) -> Optional[RichTextBlock]:
    return convert_block_ast_to_rich_text_hook.call_action(
        convert_block_ast_to_richtext_action, context, ast,
    )


def convert_block_ast_to_richtext_action(
    context: GraphQLContext, ast: dict
) -> Optional[RichTextBlock]:
    if ast["type"] == "paragraph":
        return {
            "id": get_block_id(),
            "type": "p",
            "text": convert_children_ast_to_text(context, ast["children"]),
        }

    return None


def get_block_id() -> str:
    return get_random_string(6)


def convert_children_ast_to_text(context: GraphQLContext, ast: List[dict]) -> str:
    nodes = []
    for node in ast:
        text = convert_inline_ast_to_text(context, node)
        if text is not None:
            nodes.append(text)

    return "".join(nodes)


def convert_inline_ast_to_text(context: GraphQLContext, ast: dict) -> Optional[str]:
    return convert_inline_ast_to_text_hook.call_action(
        convert_inline_ast_to_text_action, context, ast
    )


def convert_inline_ast_to_text_action(
    context: GraphQLContext, ast: dict
) -> Optional[str]:
    if ast["type"] in ("text", "inline_html"):
        return escape(ast["text"])

    if ast["type"] == "link":
        return '<a href="%s" rel="nofollow">%s</a>' % (
            escape(ast["link"]),
            convert_children_ast_to_text(context, ast["children"]),
        )

    if ast["type"] == "emphasis":
        return "<em>%s</em>" % convert_children_ast_to_text(context, ast["children"])

    if ast["type"] == "strong":
        return "<strong>%s</strong>" % convert_children_ast_to_text(
            context, ast["children"]
        )

    return None


def markup_as_html(markup: str) -> str:
    return html_markdown(markup)
