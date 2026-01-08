conversion_dict = {
    'p': ['<p', '</p>'],
    'b': ['<b', '</b>'],
    'strong': ['<strong', '</strong>'],
    'i': ['<i', '</i>'],
    'em': ['<em', '</em>'],
    'u': ['<u', '</u>'],
    'code': ['<code', '</code>'],
    'pre': ['<pre', '</pre>'],
    'span': ['<span', '</span>'],
    'div': ['<div', '</div>'],
    'h1': ['<h1', '</h1>'],
    'h2': ['<h2', '</h2>'],
    'h3': ['<h3', '</h3>'],
    'h4': ['<h4', '</h4>'],
    'h5': ['<h5', '</h5>'],
    'h6': ['<h6', '</h6>'],
    'ul': ['<ul', '</ul>'],
    'ol': ['<ol', '</ol>'],
    'li': ['<li', '</li>'],
    'a': ['<a', '</a>'],
    'img': ['<img','</img>'],
    'article': ['<article','</article>'],
    'section': ['<section','</section>']
}

class HtmlNode:
    def __init__(self, tag=None, val=None, children=None, props=None):
        self.tag = tag
        self.val = val
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __repr__(self):
        return f""" 
tag = {self.tag},
value = {self.val},
children = {[i for i in self.children]}
self.props = {self.props}
                """

    def to_html(self):
        raise NotImplementedError('not implemented here')
    
    def props_to_html(self):
        ret_str = ''
        for i in self.props:
            ret_str += f' {i}="{self.props[i]}"'
        return ret_str
    
class LeafNode(HtmlNode):
    def __init__(self, tag, val, children=None, props=None):
        super().__init__(tag, val, children, props)
        self.children = []

    def to_html(self):
        if not self.val:
            raise ValueError("No content to convert")
        if not self.tag:
            return str(self.val)
        else:
            attrs = self.props_to_html()
            return f'{conversion_dict[self.tag][0]}{attrs}>{self.val}{conversion_dict[self.tag][1]}'

    def __repr__(self):
        return f""" 
tag = {self.tag},
value = {self.val},
self.props = {self.props}
                """
    
class ParentNode(HtmlNode):
    def __init__(self, tag, val=None, children=None, props=None):
        super().__init__(tag, val, children, props)
    
    def to_html(self):
        if self.val:
            raise ValueError("parent node must have no content")
        if len(self.children)==0:
            raise ValueError("No children found for the parent node")
        else:
            cont = ''
            attrs = self.props_to_html()
            for i in self.children:
                cont+=i.to_html()
            return f'{conversion_dict[self.tag][0]}{attrs}>{cont}{conversion_dict[self.tag][1]}'