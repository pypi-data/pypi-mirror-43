#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23 9:56
# @Author  : chenjw
# @Site    : 
# @File    : html.py
# @Software: PyCharm Community Edition
# @Desc    :  do what
from base64 import b64encode


class Html:
    def __init__(self):
        self.color_red = 'color_red'
        self.color_green = 'color_green'
        self.color_blue = 'color_blue'
        self.color_grey = 'color_grey'
        self.align_right = 'right'
        self.align_left = 'left'
        self.font_b = 'b'
        # here to init different class to formate the style
        self.default_css = '''
        .table1{
            line-height: 2em;
            font-family: Arial;
            border-collapse: separate;
            border-color: #BDB76B;
        }
        .thead_tr {
            color: #000000;
            background-color: #FFFAFA;
            border-bottom: 1px solid #BDB76B;
        }
        .tbody_tr {
            color: #000000;
            font-size: 0.8em;
            background-color: #F8F8FF;
            border-bottom: 1px solid #BDB76B;
        }
        .tbody_tr:hover {
            background-color: #FFFF33;
        }
        .th1 {
            font-weight: normal;
            text-align: left;
            padding: 0 10px;
            text-align: center;
        }
        .color_red{
            background-color: #FFDAB9;
        }
        .color_green{
            background-color: #9AFF9A;
        }
        .color_blue{
            background-color: #7B68EE;
        }
        .color_grey{
            background-color: #CFCFCF;
        }
        
        .font_color_red{
            color: #FFDAB9;
        }
        .font_color_green{
            color: #9AFF9A;
        }
        .font_color_blue{
            color: #7B68EE;
        }
        .font_color_grey{
            color: #CFCFCF;
        }
        '''
        self.default_title = '测试报告'
        self.body_context = ''
        self.total_msg = ''
        pass

    def setTitle(self, title):
        '''
        :param title: name of the whole html
        :return:
        '''
        self.default_title = title
        return self

    def extraColor(self, x, y, extra=None):
        '''
        :param x: index x
        :param y: index y
        :param extra: list
        :return: None or str(color_red or color_blue or ...)
        '''
        if extra is None:
            return None
        color_list = [self.color_blue, self.color_green, self.color_grey, self.color_red]
        if isinstance(extra, list) is True:
            for sin_item in extra:
                if len(sin_item) >= 3 and \
                        isinstance(sin_item[0], int) and \
                        isinstance(sin_item[1], int) and \
                                sin_item[0] == x and \
                                sin_item[1] == y:
                    if isinstance(sin_item[2], str) and sin_item[2] in color_list:
                        return sin_item[2]
                    if isinstance(sin_item[2], list) or isinstance(sin_item[2], tuple):
                        for sin_color in sin_item[2]:
                            if sin_color in color_list:
                                return sin_color

        else:
            return None

    def extraAlign(self, x, y, extra=None):
        """
        :param x: index x
        :param y: index y
        :param extra: list
        :return: None or str(align_left or align_right or ...)
        """
        if extra is None:
            return None
        align_list = [self.align_left, self.align_right]
        if isinstance(extra, list) is True:
            for sin_item in extra:
                if len(sin_item) >= 3 and \
                        isinstance(sin_item[0], int) and \
                        isinstance(sin_item[1], int) and \
                                sin_item[0] == x and \
                                sin_item[1] == y:
                    if isinstance(sin_item[2], str) and sin_item[2] in align_list:
                        return sin_item[2]
                    if isinstance(sin_item[2], list) or isinstance(sin_item[2], tuple):
                        for sin_align in sin_item[2]:
                            if sin_align in align_list:
                                return sin_align

        else:
            return None

    def extraB(self, x, y, extra=None):
        '''
        :param x: index x
        :param y: index y
        :param extra: list
        :return: None or str(b)
        '''
        if extra is None:
            return None
        font_list = [self.font_b]
        if isinstance(extra, list) is True:
            for sin_item in extra:
                if len(sin_item) >= 3 and \
                        isinstance(sin_item[0], int) and \
                        isinstance(sin_item[1], int) and \
                                sin_item[0] == x and \
                                sin_item[1] == y:
                    if isinstance(sin_item[2], str) and sin_item[2] in font_list:
                        return sin_item[2]
                    if isinstance(sin_item[2], list) or isinstance(sin_item[2], tuple):
                        for sin_font in sin_item[2]:
                            if sin_font in font_list:
                                return sin_font

        else:
            return None

    def setTable(self, header, detail, extra=None):
        '''
        :param header: list like ['a','b','c']
        :param detail: 2D list like [['1','2','3'],['4','5','6']]
        :param extra: list like [(0,0,'color_red'),(0,0,'b')] or [(0,0,['color_red','b'])]
        :return:
        '''
        if isinstance(header, list) is False or isinstance(detail, list) is False:
            return self
        header_msg = ''
        for sin_header in header:
            header_msg += '''<th class="th1">%s</th>\n''' % sin_header
        header_msg = '''<thead><tr class="thead_tr th1">''' + header_msg + '''</tr></thead>'''
        detail_msg = ''
        for index_y in range(len(detail)):
            sin_line = detail[index_y]
            tmp_msg = ''
            for index_x in range(len(sin_line)):
                sin_cell = sin_line[index_x]
                b = self.extraB(index_x, index_y, extra)
                if b is not None:
                    sin_cell = '<b>%s</b>' % sin_cell
                color = self.extraColor(index_x, index_y, extra)
                align = self.extraAlign(index_x, index_y, extra)
                _c = 'th1'
                if color is not None:
                    _c = 'th1 %s' % color
                print(align)
                if align is None:
                    tmp_msg += '''<td class="%s">%s</td>\n''' % (_c, sin_cell)
                else:
                    tmp_msg += '''<td style="text-align:%s" class="%s">%s</td>\n''' % (align, _c, sin_cell)
                print(tmp_msg)

            detail_msg += '''<tr class="tbody_tr th1">''' + tmp_msg + '''</tr>'''
        detail_msg = '''<tbody>''' + detail_msg + '''</tbody>'''
        self.body_context += '''<table class="table1">''' + header_msg + detail_msg + '''</table>'''
        return self

    def setH(self, desc, index=6, color=None):
        '''
        :param desc: desc that to show the msg
        :param index: size
        :return:
        '''
        if color is None:
            self.body_context += '''<h%d>%s</h%d>\n''' % (index, desc, index)
        else:
            self.body_context += '''<h%d class='font_%s'>%s</h%d>\n''' % (index, color, desc, index)
        return self

    def drawBar(self, figsize=(10, 5), names=[], values=[], font=None, x_name=None, title=None, file_name=None,
                dpi=100):
        import matplotlib
        import numpy as np
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        if font is not None:
            plt.rcParams['font.family'] = [font]  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        if len(names) != len(values):
            raise Exception('len of names and len of values is not the same')
        for index in range(len(names)):
            names[index] = '%s(%s)' % (names[index], values[index])
        fig = plt.figure(figsize=figsize)
        plt.barh(np.arange(len(values)), values, color='g', alpha=0.4)
        plt.yticks(np.arange(len(values)) + 0.4, names)
        plt.grid(axis='x')
        if x_name is not None:
            plt.xlabel(x_name)
        if title is not None:
            plt.title(title)
        if file_name is not None:
            plt.savefig(file_name, dpi=dpi, bbox_inches='tight')
        plt.close()

    def setBarImg(self, figsize=(10, 5), names=[], values=[], font=None, x_name=None, title=None, dpi=100):
        file_name = 'default.png'
        self.drawBar(figsize, names, values, font, x_name, title, file_name, dpi)
        with open(file_name, 'rb') as imgFile:
            data = imgFile.read()
            self.body_context += '''<img src="%s"></img>''' % (
                'data:default/png;base64,' + str(b64encode(data), 'utf-8'))

    def draw(self, x_names=range(10), l_range=[0, 10], r_range=None, x_name=None, l_name=None, r_name='', title=None,
             l_compare=[], r_compare=[], file_name=None, dpi=100, font=None, markerSize=7):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        if font is not None:
            plt.rcParams['font.family'] = [font]  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        fig = plt.figure()
        ax = fig.add_subplot(111)
        if r_range is not None or r_compare is not None:
            ax2 = ax.twinx()
        l_lns = []
        l_markers = ['o', 's', '>', 'x']
        for _index in range(len(l_compare)):
            sin_l_compare = l_compare[_index]
            marker = l_markers[_index % len(l_markers)]
            data = sin_l_compare['data']
            label = sin_l_compare['label']
            color = sin_l_compare['color']
            lns = ax.plot(x_names, data, color, label=label, marker=marker, markerSize=markerSize)
            l_lns.append(lns)

        r_lns = []
        r_markers = ['x', '>', 's', 'o']
        for _index in range(len(r_compare)):
            sin_r_compare = r_compare[_index]
            marker = r_markers[_index % len(r_markers)]
            data = sin_r_compare['data']
            label = sin_r_compare['label']
            color = sin_r_compare['color']
            lns = ax2.plot(x_names, data, color, label=label, marker=marker, markerSize=markerSize)
            r_lns.append(lns)

        def add_lns(lns, lns_list):
            for sin_lns in lns_list:
                if lns is None:
                    lns = sin_lns
                else:
                    lns += sin_lns
            return lns

        lns = None
        lns = add_lns(lns, l_lns)
        lns = add_lns(lns, r_lns)
        labs = [l.get_label() for l in lns]

        ax.legend(lns, labs, loc=0)
        ax.grid()

        if x_name is not None:
            ax.set_xlabel(x_name)

        if l_range is not None:
            ax.set_ylim(l_range[0], l_range[1])

        if l_name is not None:
            ax.set_ylabel(l_name)
        if title is not None:
            ax.set_title(title)

        if r_range is not None:
            ax2.tick_params(axis='y', colors='red')  # 刻度颜色
            ax2.spines['right'].set_color('red')  # 纵轴颜色
            ax2.set_ylim(r_range[0], r_range[1])
            if r_name is not None:
                ax2.set_ylabel(r_name)
        if file_name is not None:
            plt.savefig(file_name, dpi=dpi, bbox_inches='tight')
        plt.close()

    def setImg(self, x_names=range(10), l_range=[0, 10], r_range=None, x_name=None, l_name=None, r_name='', title=None,
               l_compare=[], r_compare=[], dpi=100, font=None, markerSize=7):
        file_name = 'default.png'
        self.draw(x_names, l_range, r_range, x_name, l_name, r_name, title, l_compare, r_compare, file_name, dpi, font,
                  markerSize)
        with open(file_name, 'rb') as imgFile:
            data = imgFile.read()
            self.body_context += '''<img src="%s"></img>''' % (
                'data:default/png;base64,' + str(b64encode(data), 'utf-8'))

    def combine(self):
        self.total_msg = '''<!DOCTYPE html>
            <html>
            <head>
            <title>%s</title>
            <style type="text/css">
            %s
            </style>
            </head>
            <body>
            %s
            </body>
            </html>
            ''' % (self.default_title, self.default_css, self.body_context)

    def save(self, file_name):
        if self.total_msg is None or (isinstance(self.total_msg, str) and self.total_msg == ''):
            self.combine()
        with open(file_name, 'wb') as f:
            f.write(bytes(self.total_msg, 'utf-8'))


if __name__ == '__main__':
    h = Html()
    h.setTable(['122222222222', '122222222222', 'qweasad'], [['122222222222', '2333333333333', '3444']],
               extra=[(2, 0, [h.color_red, h.font_b, h.align_left])])
    h.setH('hello', 4, h.color_blue)
    h.setBarImg(names=['开始结账', '广告点击', '链接点击', '加入购物车', '购物', '曝光次数'], values=[78, 218, 3491, 13053, 19269, 1840137],
                font='SimHei', title='30天广告数据')
    h.save('a.html')
