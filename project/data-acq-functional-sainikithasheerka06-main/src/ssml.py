#!/usr/bin/env python3
"""
SSML (Speech Synthesis Markup Language) is a subset of XML specifically
designed for controlling synthesis. You can see examples of how the SSML
should be parsed in the unit tests below.
"""

#
# DO NOT USE CHATGPT, COPILOT, OR ANY AI CODING ASSISTANTS.
# Conventional auto-complete and Intellisense are allowed.
#
# DO NOT USE ANY PRE-EXISTING XML PARSERS FOR THIS TASK - lxml, ElementTree, etc.
# You may use online references to understand the SSML specification, but DO NOT read
# online references for implementing an XML/SSML parser.
#


from dataclasses import dataclass
from typing import List, Union, Dict

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(
        self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []
    ):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text
        
class _Parser: 
    def __init__(self, s: str): 
        self.s = s         
        self.i = 0            
        self.n = len(s)       

    def _peek(self) -> str: 
        return self.s[self.i] if self.i < self.n else ""  

    def _consume(self, expected: str | None = None) -> str:  
        if self.i >= self.n:                                
            raise Exception("Unexpected end of input")  
        ch = self.s[self.i]                             
        if expected is not None and ch != expected:      
            raise Exception(f"Expected '{expected}' but found '{ch}'") 
        self.i += 1                                   
        return ch                                          

    def _spaces(self):              
        while self.i < self.n and self.s[self.i].isspace(): 
            self.i += 1                                 

    def _name(self) -> str:            
        self._spaces()                 
        start = self.i                 
        while self.i < self.n and (self.s[self.i].isalnum() or self.s[self.i] in [":", "-", "_"]):  
            self.i += 1               
        if self.i == start:           
            raise Exception("Expected tag/attr name")  
        return self.s[start:self.i]     

    def _attr_value(self) -> str:    
        self._spaces()                   
        if self._peek() != '"':         
            raise Exception("Attribute values must be in double quotes") 
        self._consume('"')               
        start = self.i                     
        while self.i < self.n and self.s[self.i] != '"':  
            self.i += 1                 
        if self.i >= self.n:            
            raise Exception("Unterminated attribute value")  
        val = self.s[start:self.i]      
        self._consume('"')            
        return val                      

    def _attrs(self) -> Dict[str, str]:    
        out: Dict[str, str] = {}      
        while True:                    
            self._spaces()           
            if self._peek() in [">", "/"]: 
                break                    
            k = self._name()             
            self._spaces()           
            if self._peek() != "=":      
                raise Exception("Invalid attribute (missing '=')") 
            self._consume("=")          
            self._spaces()             
            v = self._attr_value()        
            out[k] = v                     
        return out                       

    def _text(self) -> SSMLText:        
        start = self.i                 
        while self.i < self.n and self.s[self.i] != "<":  
            self.i += 1               
        return SSMLText(unescapeXMLChars(self.s[start:self.i])) 

    def _open(self) -> tuple[str, Dict[str, str]]: 
        self._consume("<")           
        self._spaces()                 
        name = self._name()           
        self._spaces()                  
        attrs = self._attrs()             
        self._spaces()                   
        if self._peek() == "/":          
            raise Exception("Self-closing tags not supported")  
        self._consume(">")                
        return name, attrs                

    def _close(self, expected: str):      
        self._consume("<")                 
        if self._peek() != "/":          
            raise Exception("Expected closing tag")
        self._consume("/")              
        self._spaces()               
        name = self._name()              
        if name != expected:              
            raise Exception("Mismatched closing tag")  
        self._spaces()                    
        self._consume(">")                

    def _element(self) -> SSMLTag:       
        name, attrs = self._open()       
        kids: List[SSMLNode] = []          
        while True:                       
            if self.i >= self.n:          
                raise Exception("Missing closing tag")  
            if self._peek() == "<":      
                if self.i + 1 < self.n and self.s[self.i + 1] == "/":  
                    break                  
                kids.append(self._element())  
            else:
                t = self._text()           
                if t.text != "":           
                    kids.append(t)        
        self._close(name)                
        return SSMLTag(name=name, attributes=attrs, children=kids) 

    def parse(self) -> SSMLTag:            
        self._spaces()                     
        if self._peek() != "<":           
            raise Exception("Document must start with <speak>")
        node = self._element()            
        if node.name != "speak":           
            raise Exception("Top-level tag must be <speak>") 
        self._spaces()                     
        if self.i != self.n:               
            raise Exception("Only one top-level <speak> element is allowed")  
        return node 

def parseSSML(ssml: str) -> SSMLNode:
    # TODO: implement this function
    return _Parser(ssml).parse()


def ssmlNodeToText(node: SSMLNode) -> str:
    # TODO: implement this function
    if isinstance(node, SSMLText): 
        return escapeXMLChars(node.text)  
    if isinstance(node, SSMLTag):   
        attr_str = ""              
        if node.attributes:        
            attr_str = " " + " ".join(f'{k}="{v}"' for k, v in node.attributes.items())  
        inner = "".join(ssmlNodeToText(c) for c in (node.children or []))  
        return f"<{node.name}{attr_str}>{inner}</{node.name}>" 
    raise Exception("Unknown node type") 


def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def escapeXMLChars(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

# Example usage:
# ssml_string = '<speak>Hello, <break time="500ms"/>world!</speak>'
# parsed_ssml = parseSSML(ssml_string)
# text = ssmlNodeToText(parsed_ssml)
# print(text)