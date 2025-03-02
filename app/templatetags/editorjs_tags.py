from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def render_editorjs(content):
    """
    Преобразует данные Editor.js в HTML

    Пример использования: {{ article.content|render_editorjs }}
    """
    if not content or 'blocks' not in content:
        return ''

    html = []
    for block in content.get('blocks', []):
        block_type = block.get('type')
        block_data = block.get('data', {})

        if block_type == 'header':
            level = block_data.get('level', 2)
            text = block_data.get('text', '')
            html.append(f'<h{level} class="ce-header">{text}</h{level}>')

        elif block_type == 'paragraph':
            text = block_data.get('text', '')
            html.append(f'<p class="ce-paragraph">{text}</p>')

        elif block_type == 'list':
            style = block_data.get('style', 'unordered')
            items = block_data.get('items', [])

            if style == 'ordered':
                list_html = '<ol class="cdx-list">'
            else:
                list_html = '<ul class="cdx-list">'

            for item in items:
                list_html += f'<li>{item}</li>'

            list_html += '</ol>' if style == 'ordered' else '</ul>'
            html.append(list_html)

        elif block_type == 'image':
            url = block_data.get('file', {}).get('url') or block_data.get('url', '')
            caption = block_data.get('caption', '')

            figure_html = '<figure class="article-figure">'
            figure_html += f'<img src="{url}" alt="{caption}" class="article-image">'

            if caption:
                figure_html += f'<figcaption>{caption}</figcaption>'

            figure_html += '</figure>'
            html.append(figure_html)

        elif block_type == 'quote':
            text = block_data.get('text', '')
            caption = block_data.get('caption', '')
            alignment = block_data.get('alignment', 'left')

            quote_html = f'<blockquote class="cdx-quote cdx-quote--{alignment}">'
            quote_html += f'<p>{text}</p>'

            if caption:
                quote_html += f'<footer>{caption}</footer>'

            quote_html += '</blockquote>'
            html.append(quote_html)

        elif block_type == 'delimiter':
            html.append('<hr class="ce-delimiter">')

        elif block_type == 'table':
            rows = block_data.get('content', [])

            table_html = '<table class="ce-table">'
            for row in rows:
                table_html += '<tr>'
                for cell in row:
                    table_html += f'<td>{cell}</td>'
                table_html += '</tr>'
            table_html += '</table>'

            html.append(table_html)

    return mark_safe('\n'.join(html))
