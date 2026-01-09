import re

from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode

def main():
    to = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(to)


if __name__ == '__main__':
    main()