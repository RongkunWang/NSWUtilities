#!/bin/usr/env python3
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from collections import OrderedDict

import json
from .JsonModules import merge_dict
from .JsonModules import sort_dict

class BoardObj(object):
    def __init__(self, fin_name):
        self._fin_name = fin_name
        with open(fin_name) as fin:
            raw_data = json.load(fin)
            fin.close()
        self._boards = OrderedDict()
        self._vmm_key = "vmm_common_config"
        self._tds_key = "tds_common_config"
        self._roc_key = "roc_common_config"
        self._roc_d_key = "rocCoreDigital"
        self._roc_a_key = "rocPllCoreAnalog"
        self._commons = {
                self._vmm_key:{},
                self._roc_key:{
                    self._roc_a_key:{},
                    self._roc_d_key:{},
                    },
                self._tds_key:{},
                }
        for key in raw_data.keys():
            if self._vmm_key == key:
                self._commons[self._vmm_key] = sort_dict(raw_data[self._vmm_key])
                continue
            if self._tds_key == key:
                self._commons[self._tds_key] = sort_dict(raw_data[self._tds_key])
                continue
            if self._roc_key == key:
                self._commons[self._roc_key][self._roc_a_key] = sort_dict(raw_data[self._roc_key][self._roc_a_key])
                self._commons[self._roc_key][self._roc_d_key] = sort_dict(raw_data[self._roc_key][self._roc_d_key])
                continue
            if key[:4] not in ["SFEB", "PFEB", "MMFE"]:
                continue
            self._boards[key] = raw_data[key]

        self._supplement()

        pass

    def return_type_of_board(self, board):
        vmmRange = range(8)
        tdsRange = range(4)
        if "MMFE" == board[:4]:
            tdsRange = []
        if "SFEB6" == board[:5]:
            vmmRange = range(2, 8)
            tdsRange = range(1, 4)
        if "PFEB"  == board[:4]:
            vmmRange = range(3)
            tdsRange = range(1)
        return vmmRange, tdsRange

    def _supplement(self,):
        for board, l_chip in self._boards.items():
            # covers SFEB8 SFEB
            vmmRange, tdsRange = self.return_type_of_board(board)

            for chip, chip_reg in l_chip.items():
                if self._roc_d_key == chip:
                    self._boards[board][chip] = merge_dict(chip_reg, self._commons[self._roc_key][self._roc_d_key])
                    continue
                if self._roc_a_key == chip:
                    self._boards[board][chip] = merge_dict(chip_reg, self._commons[self._roc_key][self._roc_a_key])
                    #  print(self._commons[self._roc_key][self._roc_a_key])
                    #  print(self._boards[board][chip])
                    #  print()
                pass

            for i in vmmRange:
                chip = "vmm{0}".format(i) 
                if chip not in self._boards[board]: 
                    self._boards[board][chip] = {}
                self._boards[board][chip] = merge_dict(self._boards[board][chip],
                        self._commons[self._vmm_key])

            for i in tdsRange:
                chip = "tds{0}".format(i)
                if chip not in self._boards[board]: 
                    self._boards[board][chip] = {}
                self._boards[board][chip] = merge_dict(self._boards[board][chip],
                        self._commons[self._tds_key])
            pass
        pass

    def debug_print(self):
        print("vmm common", self._commons[self._vmm_key])
        print("tds common", self._commons[self._tds_key])
        print("roc digital common", self._commons[self._roc_key][self._roc_d_key])
        print("vmm analog common", self._commons[self._roc_key][self._roc_a_key])
        print("")
        pass

    @property
    def boards(self):
        #  print("property")
        return self._boards

    @boards.setter
    def boards(self, dict):
        #  print("property setter")
        self._boards = dict

    def apply_one_board(self, name, new_reg):
        #  print("apply one")
        self.boards[name] = merge_dict(new_reg, self.boards[name])

    def dump(self, name):
        with open(name, 'w') as fp:
            out = OrderedDict()
            out.update(self._commons)
            #  tmp1 = json.dumps(self._commons, indent=4, sort_keys = False)
            out.update(sort_dict(self.boards))
            #  OrderedDict(sorted(self.boards.items()))
            #  od = collections.OrderedDict(sorted(d.items()))
            #  tmp2 = json.dumps(self.boards, indent=4, sort_keys = True)
            tmp2 = json.dump(out, fp, indent=4, sort_keys = False)
            #  fp.write(tmp1[:-1])
            #  fp.write(tmp2[1:])
            fp.close()

    pass
