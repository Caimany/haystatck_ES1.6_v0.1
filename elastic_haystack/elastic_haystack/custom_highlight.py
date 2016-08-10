# # encoding: utf-8
#
#
# from django.utils.html import strip_tags
#
# text_block="""
# 杨学玲：“感谢工会，钱到账了，好开心。”。范焕坚 摄 2月2日，在广州越秀干休所所部新建工程项目部任资料员的杨学玲，致电荔湾区建筑工地工会联合会副主席范焕坚表示，广东五华一建工程有限公司已按赔付协议，将5万元划入了她指定的账户。 同一天，总承包单位越秀干休所所部新建工程的广东五华一建工程有限公司财务人员也致电范焕坚，报告赔付金已通过银行划账，结付给杨学玲。 这两个电话，揭开了一宗经“四方协商”追讨欠薪的维权故事。 怀孕女工求助工会 2015年10月的一天，范焕坚接到一宗由区内建筑工地工人反映工资维权未果的案件。范焕坚当即联系上当事人杨学玲，向她了解情况。 “胳膊拧不过大腿啊!”怀有身孕的杨学玲见到工会人顿时大哭，仿佛找到了靠山，之前追讨工资遭受的委屈，如打开缺口的大堤哗啦啦尽情释放，恳求工会出面帮忙。 杨学玲诉说，从2013年5月13日起，她受雇于广东五华一建工程有限公司名义下的越秀干休所所部新建工程项目部任资料员。该工合同竣工时间为2014年1月28日。因工期延误，当年9月6日项目部工作进入收尾阶段，当时杨学玲是辞退剩下的4名工人之一。 经过多番催讨，老板才结清她2014年的工资。之后，从2015年1月到10月期间，老板一直没正常给她发工资。杨学玲自己算过账，老板共欠她工资约58000元。 范焕坚把情况汇报到广州市建筑工地工联会。工联会主席钟坚军考虑到该工程项目的管辖地在天河区，于是请天河区建筑工地工联会主席梁广一齐开展维权行动。 接着，范焕坚又根据杨学玲反映的情况，与她一起分析案情，计算她的日工资、工作天数等，梳理成未按规定签订劳动合同;未按规定购买社保、医保;未按约定支付工资;拖欠或者克扣工资;侵害工资报酬权益的其他行为;按规定在杨学玲怀孕期间，用人单位不得解除她的劳动合同等几大维权要点。 四方协商达成庭外和解 “欠薪属于恶劣违法侵权行为，该争取的权益一定要努力争取。”范焕坚为杨学玲打气，告诉她根据相关法规，用人单位应足额支付金额为：12.9万元。杨学玲同意，以12.9万元赔偿金额为协商目标。 11月3日上午，范焕坚与梁广及当事人杨学玲一起，踏进广东五华一建广州办事处，希望双方能和平协商解决问题。然而，却被一颗软钉子，刺得很不是滋味。 先是办事处一位工作人员说，工地负责人不在，将范焕坚等3人晾了大半天，后又以负责人没空为由驱赶，甚至口出 “有本事就去上告”等狂言。此后，一连3天都是如此。 上门协商不成，范焕坚和梁广合议后，建议杨学玲向项目所在地天源街劳监中队请求帮助。 2015年11月11日，经天源街劳监中队人员协调，劳资双方终于能坐下来协商解决杨学玲欠薪问题了。但是，由于双方意见分歧过大，未能提出解决方案。 考虑到杨学玲怀孕已多月，经不起来回奔波无休止的折腾和精神心理的多重压力，范焕坚、梁广分头了解双方的底线和意愿并作沟通、劝说，希望双方理性化解分歧，尽可能找彼此都能接受的平衡量。 后来，在天源街劳监中队协调之下，工程项目方接受工联会和杨学玲提出的赔付要求达成庭外和解协议。工程项目方在2016年春节前，首期赔付杨学玲5万元人民币。 （编辑：苏卓图）
# """
#
# query="广东"
# query_words = set([word.lower() for word in query.split() if not word.startswith('-')])
# SYMBOL='。'
# def find_symbol(text_block):
#     word_positions = {}
#
#     # Pre-compute the length.
#     end_offset = len(text_block)
#     lower_text_block = text_block.lower()
#     for word in ['。', '\n']:
#         if not word in word_positions:
#             word_positions[word] = []
#
#         start_offset = 0
#
#         while start_offset < end_offset:
#             next_offset = lower_text_block.find(word, start_offset, end_offset)
#
#             # If we get a -1 out of find, it wasn't found. Bomb out and
#             # start the next word.
#             if next_offset == -1:
#                 break
#
#             word_positions[word].append(next_offset)
#             start_offset = next_offset + len(word)
#     symbol_location_list=word_positions[SYMBOL]
#     symbol_location_list.insert(0,0)
#     symbol_location_list.sort()
#     return symbol_location_list
#
# start_offset=1000
#
# symbol_location_list=find_symbol(text_block)
# print symbol_location_list
#
# for i in range(0,len(symbol_location_list)-2):
#     if symbol_location_list[i]>symbol_location_list[-1]:
#         #越界了
#         break
#     if symbol_location_list[i]<start_offset and symbol_location_list[i+1]>start_offset:
#         start_offset_ext=symbol_location_list[i]
#         end_off_ext=symbol_location_list[i+1]
#         break
#
# print(start_offset_ext,end_off_ext)
#
#
#
# def combine_index_windows(index_windows):
#     combine_index_windows = []
#     combine_index_windows_final = []
#     for i in index_windows:
#         combine_index_windows.append(i[0])
#         combine_index_windows.append(i[1])
#     # return combine_index_windows
#     i = 0
#     while i < len(combine_index_windows) - 1:
#         if combine_index_windows[i] != combine_index_windows[i + 1]:
#
#             combine_index_windows_final.append(combine_index_windows[i])
#             i = i + 1
#         else:
#             i = i + 2
#     combine_index_windows_final.append(combine_index_windows[len(combine_index_windows) - 1])
#     return combine_index_windows_final
