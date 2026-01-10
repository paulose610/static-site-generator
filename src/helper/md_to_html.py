from src.helper.block_helper import block_to_block_type, BlockType, markdown_to_blocks
from src.helper.htmlnode import LeafNode, ParentNode
from src.helper.inline_helper import text_to_textnodes, text_node_to_html_node
#from src.textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = process_blocks(blocks)

    html_node = ParentNode(tag='div')
    html_node.children = block_nodes
    
    return html_node


def process_blocks(blocks):
    block_nodes = []
    
    for i in blocks:
        block_type = block_to_block_type(i)
        block_node=None
        block_children=None
        match block_type:
            case BlockType.PARA:
                block_node = ParentNode(tag='p')
                block_children = get_block_children(i,BlockType.PARA)
                block_node.children = block_children
            case BlockType.CODE:
                block_node = ParentNode(tag='pre',val=None,children=[LeafNode(tag='code',val=i.split('```',2)[1][1:])])
            case BlockType.HEADING:
                head_count = 0
                for c in i:
                    if c=='#':
                        head_count+=1
                    if c=='\n':
                        break
                head_tag = f'h{head_count}'
                block_node = ParentNode(tag=head_tag)
                block_children = get_block_children(i,BlockType.HEADING)
                block_node.children = block_children
            case BlockType.UO_LIST:
                block_node = ParentNode(tag='ul')
                block_children = get_block_children(i,BlockType.UO_LIST)
                block_node.children = block_children
            case BlockType.O_LIST:
                block_node = ParentNode(tag='ol')
                block_children = get_block_children(i,BlockType.O_LIST)
                block_node.children = block_children
            case BlockType.QUOTE:
                block_node = ParentNode(tag='quote')
                block_children = get_block_children(i,BlockType.QUOTE)
                block_node.children = block_children
            
        block_nodes.append(block_node)
    
    return block_nodes


def get_block_children(block,block_type):
    children = []
    for i in block.split('\n'):
        i_node = None
        i_children = []
        match block_type:
            case BlockType.PARA:
                i_children = text_to_textnodes(i)
                i_node = ParentNode(tag=None,val=None) if len(i_children)>1 else LeafNode(tag=None,val=i)
            case BlockType.HEADING:
                i=i.split(' ',1)[1]
                i_children = text_to_textnodes(i)
                i_node = ParentNode(tag=None,val=None) if len(i_children)>1 else LeafNode(tag=None,val=i)
            case BlockType.UO_LIST:
                i=i.split(' ',1)[1]
                i_children = text_to_textnodes(i)
                i_node = ParentNode(tag='li',val=None) if len(i_children)>1 else LeafNode(tag='li',val=i)
            case BlockType.O_LIST:
                i=i.split(' ',1)[1]
                i_children = text_to_textnodes(i)
                i_node = ParentNode(tag='li',val=None) if len(i_children)>1 else LeafNode(tag='li',val=i)
            case BlockType.QUOTE:
                i=i.split(' ',1)[1]
                i_children = text_to_textnodes(i)
                i_node = ParentNode(tag=None,val=None) if len(i_children)>1 else LeafNode(tag=None,val=i)
                
        if i_node:
            if len(i_children)>1:
                i_children = list(map(lambda x: text_node_to_html_node(x), i_children))
                i_node.children = i_children
        children.append(i_node)
    return children
            