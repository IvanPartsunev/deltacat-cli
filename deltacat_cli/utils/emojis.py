"""Emoji configuration for CLI output."""

# Professional emoji set - clean and monochrome-friendly
EMOJIS = {
    'loading': '→',  # Loading/processing
    'success': '✓',  # Success/completed
    'error': '✗',  # Error/failed
    'warning': '!',  # Warning/attention
    'info': '·',  # Info/neutral
    'empty': '○',  # Empty/none found
    'list': '▪',  # List item
    'catalog': '◆',  # Catalog related
    'namespace': '▫',  # Namespace related
    'table': '▪',  # Table related
}

# Alternative sets you can switch to:
EMOJI_SETS = {
    'professional': {
        'loading': '→',
        'success': '✓',
        'error': '✗',
        'warning': '!',
        'info': '·',
        'empty': '○',
        'list': '▪',
        'catalog': '◆',
        'namespace': '▫',
        'table': '▪',
    },
    'geometric': {
        'loading': '◐',
        'success': '●',
        'error': '●',
        'warning': '◯',
        'info': '◆',
        'empty': '○',
        'list': '▪',
        'catalog': '◆',
        'namespace': '◇',
        'table': '▪',
    },
    'minimal': {
        'loading': '·',
        'success': '✓',
        'error': '✗',
        'warning': '!',
        'info': '·',
        'empty': '∅',
        'list': '·',
        'catalog': '·',
        'namespace': '·',
        'table': '·',
    },
    'colorful': {  # Original colorful emojis
        'loading': '🔄',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'empty': '📭',
        'list': '📋',
        'catalog': '📚',
        'namespace': '📁',
        'table': '📊',
    },
}


def get_emoji(name: str) -> str:
    """Get emoji by name."""
    return EMOJIS.get(name, '·')


def set_emoji_style(style: str) -> None:
    """Switch to a different emoji style."""
    global EMOJIS
    if style in EMOJI_SETS:
        EMOJIS.update(EMOJI_SETS[style])
