from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode

def main():
    to = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(to)

def text_node_to_html_node(node):
    match node.type:
        case TextType.TEXT:
            return LeafNode(None,node.text)
        case TextType.BOLD:
            return LeafNode('b',node.text)
        case TextType.CODE:
            return LeafNode('code',node.text)
        case TextType.ITALIC:
            return LeafNode('i',node.text)
        case TextType.LINK:
            return LeafNode('a',node.text,None,{'href':node.url})
        case TextType.IMAGE:
            return LeafNode('i',None,None,{'src':node.url,'alt':node.alt})
        case _:
            raise ValueError('No such TextType') 

if __name__ == '__main__':
    main()