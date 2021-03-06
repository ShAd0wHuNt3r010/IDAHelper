from idautils import *
from idaapi import *
from idc import *


class StaticAnalysis:
    registers = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp']

    def __init__(self):
        return

    def get_args_of_functions(self, address_of_func, number_of_args):
        if number_of_args <= 0:
            return

        args_of_functions = {}

        xref = CodeRefsTo(address_of_func, 1)
        for address in xref:
            args_of_functions[address] = self.get_args_of_function(address, number_of_args)

        return args_of_functions

    @staticmethod
    def get_args_of_function(address, number_of_args):
        if number_of_args <= 0:
            return

        args_f = [None] * number_of_args
        arg_counter = 0

        for i in range(0, 10):
            address = PrevHead(address, 0)
            if arg_counter == number_of_args:
                break
            if GetMnem(address) == 'push':
                if GetOpType(address, 0) == idaapi.o_imm:
                    args_f[arg_counter] = GetOperandValue(address, 0)
                else:
                    args_f[arg_counter] = GetOpnd(address, 0)
                arg_counter += 1

        return args_f

    @staticmethod
    def get_flow_chart(address):
        start_func = GetFunctionAttr(address, FUNCATTR_START)
        return idaapi.FlowChart(idaapi.get_func(start_func))

    @staticmethod
    def get_block_id(flow_chart, specific_address):
        for index in range(0, flow_chart.size):
            block = flow_chart[index]
            if block.endEA > specific_address >= block.startEA:
                return index

    @staticmethod
    def get_block_start_address(flow_chart, specific_address):
        for index in range(0, flow_chart.size):
            block = flow_chart[index]
            if block.endEA > specific_address >= block.startEA:
                return block.startEA

    @staticmethod
    def get_block_end_address(flow_chart, specific_address):
        for index in range(0, flow_chart.size):
            block = flow_chart[index]
            if block.endEA > specific_address >= block.startEA:
                return block.endEA

    @staticmethod
    def is_add_in_func(func_start_add, address):
        if GetFunctionAttr(address, FUNCATTR_START) == func_start_add:
            return True
        else:
            return False

    @staticmethod
    def find_ins_txt(address, ins_str):
        res_list = []
        while 1:
            address = FindText(address, SEARCH_DOWN, 0, 0, ins_str)
            if address == BADADDR:
                break
            res_list.append(address)
            address = NextHead(int(address))
            if address == BADADDR:
                break
        return res_list
