from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_h1_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "# Hello world!")
    assert result == [{"id": ANY, "type": "h1", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_h1_alternate_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello world!\n====")
    assert result == [{"id": ANY, "type": "h1", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_h2_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello world!\n----")
    assert result == [{"id": ANY, "type": "h2", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_h2_alternate_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "## Hello world!")
    assert result == [{"id": ANY, "type": "h2", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_h3_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "### Hello world!")
    assert result == [{"id": ANY, "type": "h3", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_h4_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "#### Hello world!")
    assert result == [{"id": ANY, "type": "h4", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_h5_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "##### Hello world!")
    assert result == [{"id": ANY, "type": "h5", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_h6_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "###### Hello world!")
    assert result == [{"id": ANY, "type": "h6", "text": "Hello world!",}]


@pytest.mark.asyncio
async def test_quote_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "> Hello world!")
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "children": [{"id": ANY, "type": "p", "text": "Hello world!",}],
        }
    ]


@pytest.mark.asyncio
async def test_code_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "```\nconsole.log('test')\n```")
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": None,
            "text": "console.log(&#x27;test&#x27;)\n",
        }
    ]


@pytest.mark.asyncio
async def test_code_markdown_with_syntax_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "```python\nprint('test')\n```")
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": "python",
            "text": "print(&#x27;test&#x27;)\n",
        }
    ]


@pytest.mark.asyncio
async def test_code_markdown_escapes_text(graphql_context):
    result, _ = await parse_markup(graphql_context, "```\n<script>\n```")
    assert result == [
        {"id": ANY, "type": "code", "syntax": None, "text": "&lt;script&gt;\n",}
    ]


@pytest.mark.asyncio
async def test_horizontal_line_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello\n- - -\nWorld")
    assert result == [
        {"id": ANY, "type": "p", "text": "Hello",},
        {"id": ANY, "type": "hr",},
        {"id": ANY, "type": "p", "text": "World",},
    ]


@pytest.mark.asyncio
async def test_ordered_list_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "1. Lorem\n2. Ipsum")
    assert result == [
        {
            "id": ANY,
            "type": "list",
            "ordered": True,
            "children": [
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Lorem"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Ipsum"}],
                },
            ],
        },
    ]


@pytest.mark.asyncio
async def test_unordered_list_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "- Lorem\n- Ipsum")
    assert result == [
        {
            "id": ANY,
            "type": "list",
            "ordered": False,
            "children": [
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Lorem"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Ipsum"}],
                },
            ],
        },
    ]


@pytest.mark.asyncio
async def test_nesting_lists_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(
        graphql_context,
        (
            "1. Apple\n"
            "2. Orange\n"
            "    1. Banana\n"
            "    2. Lemon\n"
            "3. Tomato\n"
            "4. Potato\n"
        ),
    )
    assert result == [
        {
            "id": ANY,
            "type": "list",
            "ordered": True,
            "children": [
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Apple"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [
                        {"id": ANY, "type": "f", "text": "Orange"},
                        {
                            "id": ANY,
                            "type": "list",
                            "ordered": True,
                            "children": [
                                {
                                    "id": ANY,
                                    "type": "li",
                                    "children": [
                                        {"id": ANY, "type": "f", "text": "Banana",}
                                    ],
                                },
                                {
                                    "id": ANY,
                                    "type": "li",
                                    "children": [
                                        {"id": ANY, "type": "f", "text": "Lemon"}
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Tomato"}],
                },
                {
                    "id": ANY,
                    "type": "li",
                    "children": [{"id": ANY, "type": "f", "text": "Potato"}],
                },
            ],
        },
    ]
