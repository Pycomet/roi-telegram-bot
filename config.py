import os
from flask import Flask, request
import telebot
from telebot import types
import emoji

# Bot token information
TOKEN = '1027166109:AAH-VqLwJLRNfbPegg3hqFjdxrI6z0z4oGU'

# Database Url
DATABASE_URL = "postgres://ejjtgsuaguhtru:e8f8c4aec67b246f9315576c50e1306bfe8cdefb64520c5b44065f034b8e30c3@ec2-52-7-39-178.compute-1.amazonaws.com:5432/daokl2gmp4eef"

# CoinBase API information
API_KEY = "euAAnrDNp00ZhU5V"

API_SECRET = "GjNojkpCtycOt7YahpXWndG6uv1oEoXr"


# Refrenced wallet for investment splitting
BTC_TRADE_ADDRESS = ""
XRP_TRADE_ADDRESS = ""

BTC_ADMIN_ADDRESS = ""
XRP_ADMIN_ADDRESS = ""


