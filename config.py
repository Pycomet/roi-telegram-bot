import os
from flask import Flask, request
import telebot
from telebot import types
import emoji
from decouple import config

# Bot token information
TOKEN = config("TOKEN")

# Database Url
DATABASE_URL = config("DATABASE_URL")

# CoinBase API information
API_KEY = config("API_KEY")

API_SECRET = config("API_SECRET")


# Refrenced wallet for investment splitting
BTC_TRADE_ADDRESS = ""
XRP_TRADE_ADDRESS = ""

BTC_ADMIN_ADDRESS = ""
XRP_ADMIN_ADDRESS = ""


