# -*- coding:utf-8 -*-
import sys,json
reload(sys)
sys.setdefaultencoding('utf8')

from haystack.utils import Highlighter

SYMBOL='。'

def find_symbol(text_block):
    word_positions = {}

    # Pre-compute the length.
    end_offset = len(text_block)
    lower_text_block = text_block.lower()
    # 测试
    for word in ['。', '\n']:
        if not word in word_positions:
            word_positions[word] = []

        start_offset = 0

        while start_offset < end_offset:
            # print word
            next_offset = lower_text_block.find(word, start_offset, end_offset)

            # If we get a -1 out of find, it wasn't found. Bomb out and
            # start the next word.
            if next_offset == -1:
                break

            word_positions[word].append(next_offset)
            start_offset = next_offset + len(word)
    symbol_location_list=word_positions[SYMBOL]
    symbol_location_list.insert(0,0)
    symbol_location_list.insert(-1,len(text_block))
    symbol_location_list.sort()
    return symbol_location_list

class CustomHighlighter(Highlighter):

    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        # Start by chopping the block down to the proper window.
        text = self.text_block[start_offset:end_offset]

        # Invert highlight_locations to a location -> term list
        term_list = []

        for term, locations in highlight_locations.items():
            term_list += [(loc - start_offset, term) for loc in locations]

        loc_to_term = sorted(term_list)

        # Prepare the highlight template
        if self.css_class:
            hl_start = '<%s class="%s">' % (self.html_tag, self.css_class)
        else:
            hl_start = '<%s>' % (self.html_tag)

        hl_end = '</%s>' % self.html_tag

        # Copy the part from the start of the string to the first match,
        # and there replace the match with a highlighted version.
        highlighted_chunk = ""
        matched_so_far = 0
        prev = 0
        prev_str = ""

        for cur, cur_str in loc_to_term:
            # This can be in a different case than cur_str
            actual_term = text[cur:cur + len(cur_str)]

            # Handle incorrect highlight_locations by first checking for the term
            if actual_term.lower() == cur_str:
                if cur < prev + len(prev_str):
                    continue

                highlighted_chunk += text[prev + len(prev_str):cur] + hl_start + actual_term + hl_end
                prev = cur
                prev_str = cur_str

                # Keep track of how far we've copied so far, for the last step
                matched_so_far = cur + len(actual_term)

        # Don't forget the chunk after the last term
        highlighted_chunk += text[matched_so_far:]
        symbol_location_list = find_symbol(self.text_block)

        # print highlight_locations.items()
        start_offset_ext=start_offset
        end_offset_ext=end_offset
        for i in range(0, len(symbol_location_list)-1):

            # if  symbol_location_list[i] < start_offset:
            #     print symbol_location_list[i],symbol_location_list[i+1],"%%%%"
            if symbol_location_list[i+1]>start_offset:

                    start_offset_ext = symbol_location_list[i]
                    end_offset_ext = symbol_location_list[i + 1]
                    break
        if start_offset-start_offset_ext>50:
            start_offset_ext=start_offset-50

        if end_offset_ext-end_offset>50:
            end_offset_ext=end_offset+50

        if end_offset_ext>end_offset:
            highlighted_chunk=self.text_block[start_offset_ext:start_offset]+highlighted_chunk
        else:
            highlighted_chunk=self.text_block[start_offset_ext:start_offset]+highlighted_chunk+self.text_block[end_offset:end_offset_ext]


        if start_offset_ext > 0:
            highlighted_chunk = '。。%s' % highlighted_chunk

        if end_offset_ext < len(self.text_block):
            highlighted_chunk = '%s。。。' % highlighted_chunk

        return highlighted_chunk