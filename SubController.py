from flask import Flask, render_template, redirect, request,  url_for, session, json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.sql import select, insert

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/student")

conn = engine.connect()


def subtotal(itemId, size, toppingList, quantity):
    subtotal = 0
    quantity = int(quantity)
    if size == 'M':
        with open('documents/subtotal_findById_items.txt', 'r') as txt:
            itemselect = text(txt.readline())
            connItem = conn.execute(itemselect, {"itemId": itemId})
            for item in connItem:
                itemtotal = item.price_m
            subtotal = (itemtotal + len(toppingList)*200)*quantity
        return subtotal

        # for item in connItem:
        #     for topping in toppingList:
        #         with open('documents/subtotal_findById_toppings.txt', 'r') as txt:
        #             toppingselect = text(txt.readline())
        #             connTopping = conn.execute(
        #                 toppingselect, {"toppingId": topping})
        #             for topping in connTopping:
        #                 subtotal += topping.price_m
        #     subtotal += item.price_m
        # subtotal = subtotal * quantity
    else:
        with open('documents/subtotal_findById_items.txt', 'r') as txt:
            itemselect = text(txt.readline())
            connItem = conn.execute(itemselect, {"itemId": itemId})
            for item in connItem:
                itemtotal = item.price_m
            subtotal = (itemtotal + len(toppingList)*300)*quantity
        return subtotal
        # for topping in toppingList:
        #     with open('documents/subtotal_findById_toppings.txt', 'r') as txt:
        #         toppingselect = text(txt.readline())
        #         connTopping = conn.execute(
        #             toppingselect, {"toppingId": topping})
        #         print(connTopping)
        #         for topping in connTopping:
        #             subtotal += topping.price_l
        #     subtotal += item.price_l
        # subtotal = subtotal * quantity
        # print(subtotal)
