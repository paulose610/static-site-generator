from enum import Enum
import re


class BlockType(Enum):
    PARA = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UO_LIST = 'unordered list'
    O_LIST = 'ordered list'

def markdown_to_blocks(md):
    blocks = list(
                filter(
                    lambda x: x,
                    list(
                        map(
                            lambda x: x.strip(),
                            md.split("\n\n")
                            )
                        )
                    )
                )
    return blocks

def block_to_block_type(block):
    quote_count = 0
    uo_list_count = 0
    o_list_count = 1
    
    block_line = block.split('\n')
    block_size = len(block_line)
    
    if block_size==1 and re.search(r'^#{1,6} .*$',block_line[0]):
        return BlockType.HEADING
    if block_line[0] == '```' and block_line[-1]=='```':
        return BlockType.CODE
    
    for i in block_line:
        if i.startswith('> '):
            quote_count+=1
        elif i.startswith('- '):
            uo_list_count+=1
        elif i.startswith(f'{o_list_count}. '):
            o_list_count+=1
    
    if quote_count==block_size:
        return BlockType.QUOTE
    elif o_list_count==block_size+1:
        return BlockType.O_LIST
    elif uo_list_count==block_size:
        return BlockType.UO_LIST
    
    return BlockType.PARA
