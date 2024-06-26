import streamlit as st
import re

def normalize(s):
    return (''.join((' ' + c + ' ' if c in '*/+-=()' else c for c in s.replace('**', '^').replace(' ', ''))).replace('^', ' ** ')).replace(' * -', ' *-')

def mostNested(s):
    return max(enumerate([sum([1 if c == '(' else -1 if c == ')' else 0 for c in s[:i+1]]) for i in range(len(s))]), key=lambda x: x[1])[0]

def extractSubstring(s):
    x = mostNested(s)
    i = s.index(')', x) + 1 if ')' in s[x:] else len(s)
    result = (s[x+1:i-1]).strip()
    evaluated = eval(result)
    st.write(f'{result} = {evaluated}')
    return result, s[:x] + str(evaluated) + s[i:]

def extraction(s):
    s = normalize(s)
    while '(' in s:
        e, s = extractSubstring(s)
    return eval(normalize(s))

st.title('Math Expression Evaluator')
input_string = st.text_input('Enter your expression:', '', max_chars=None, help='Allowed characters: 0-9, +, -, *, /, ^, (, )')
filtered_string = ''.join([char for char in input_string if char in '/*-+0123456789.^() '])

if st.button('Evaluate'):
    result = extraction(filtered_string)
    st.write(f'Result: {result}')
