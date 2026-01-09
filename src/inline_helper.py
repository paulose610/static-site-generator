import re
import pprint

from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode


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
            return LeafNode('i',None,None,{'src':node.url,'alt':node.text})
        case _:
            raise ValueError('No such TextType')
        
def splits_nodes_delimiter(nodes,delimiter,textType):
    new_nodes = []
    if nodes[0].type!=TextType.TEXT:
        new_nodes.append(nodes[0])
    else:
        new_nodes = [
            TextNode(part, textType) if i % 2 == 1 else TextNode(part, TextType.TEXT)
            for i, part in enumerate(nodes[0].text.split(delimiter))
        ]

        if len(new_nodes)%2==0:
            raise ValueError(f"No closing delimter found for {nodes[0].text}")
        if new_nodes[-1].text=='':
            new_nodes=new_nodes[:-1]
        if new_nodes[0].text=='':
            new_nodes=new_nodes[1:]    

    for i in range(1,len(nodes)):
        if nodes[i].type!=TextType.TEXT:
            new_nodes.append(nodes[i]) 
        else:
            new = [
                TextNode(part, textType) if i % 2 == 1 else TextNode(part, TextType.TEXT)
                for i, part in enumerate(nodes[i].text.split(delimiter))
            ]
            if len(new)%2==0:
                raise ValueError(f"No closing delimter {delimiter} found for {nodes[i].text}")
            if new[-1].text=='':
                new=new[:-1]
            if new[0].text=='':
                new=new[1:]
            new_nodes.extend(new)
    return new_nodes

def extract_markdown_images(text):
    x = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return x

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)

def split_nodes_images_or_links(nodes,type):
    extract_func = extract_markdown_images if type==TextType.IMAGE else extract_markdown_links
    regex_splitter = r"(!\[.*?\]\(.*?\))" if type==TextType.IMAGE else r"(\[.*?\]\(.*?\))"
    new_nodes = []
    if nodes[0].type!=TextType.TEXT:
        new_nodes.append(nodes[0])
    else:
        new_nodes = [
            TextNode(part, TextType.TEXT) if i % 2 == 0 else TextNode(extract_func(part)[0][0], type, extract_func(part)[0][1])
            for i, part in enumerate(re.split(regex_splitter,nodes[0].text))
        ]
        if len(new_nodes)%2==0:
            raise ValueError(f"No Image found for {nodes[0].text}")
        if new_nodes[-1].text=='':
            new_nodes=new_nodes[:-1]
        if new_nodes[0].text=='':
            new_nodes=new_nodes[1:]    
   
    for i in range(1,len(nodes)):
        if nodes[i].type!=TextType.TEXT:
            new_nodes.append(nodes[i]) 
        else:
            new = [
                TextNode(part, TextType.TEXT) if i % 2 == 0 else TextNode(extract_func(part)[0][0], type, extract_func(part)[0][1])
                for i, part in enumerate(re.split(regex_splitter,nodes[i].text))
            ]
            if len(new)%2==0:
                raise ValueError(f"No Image found for {nodes[i].text}")
            if new[-1].text=='':
                new=new[:-1]
            if new[0].text=='':
                new=new[1:]
            new_nodes.extend(new)

    return [
        x for x in new_nodes
        if not (x.type == TextType.TEXT and not x.text)
    ]


def text_to_textnodes(text):
    nodes = splits_nodes_delimiter([TextNode(text,TextType.TEXT)],"**",TextType.BOLD)
    nodes = splits_nodes_delimiter(nodes,"_",TextType.ITALIC)
    nodes = splits_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = split_nodes_images_or_links(nodes,TextType.IMAGE)
    nodes = split_nodes_images_or_links(nodes,TextType.LINK)
    return nodes

