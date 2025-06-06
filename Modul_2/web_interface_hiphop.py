#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 15:46:04 2025

@author: rabeawu
"""
import streamlit as st
import pyterrier as pt
import pickle
import os


if not pt.java.started():
    pt.java.init()
    
st.set_page_config(page_title="Bibsonomy Hiphop-Data", page_icon=":musical_note:")
st.title("Search in Bibsonomy Hiphop-Data")

INDEX_PATH = os.getcwd() + "/index_hiphop/data.properties"
DATA_PATH = os.getcwd() + "/hiphop_search.pkl"


def init():

    index = pt.IndexFactory.of(INDEX_PATH)
    st.session_state["engine"] = pt.BatchRetrieve(index, wmodel="Tf")
    st.session_state["data"] = pickle.load(open(DATA_PATH, "rb"))


def search(query):

    res = st.session_state["engine"].search(query)
    fields_to_show = ['text', 'authors', 'year', 'url', 'abstract', 'tags', 'id']

    for _, row in res.iterrows():
        score = round(row['score'], 2)
        sel_entry = st.session_state["data"][st.session_state["data"]['docno'] == row['docno']]
        if sel_entry.empty:
            continue
      
        entry = sel_entry.iloc[0]

        for field in fields_to_show:
            if field == "text":
                st.title(entry[field])
            else:
                st.write(f"{field.capitalize()}: \t {entry[field]}")

        st.write(f"Score: {score}")
        st.divider()


if not "engine" in st.session_state:
    init()

query = st.sidebar.text_input(" ", help="write your search query inside the form", placeholder="search query")
st.sidebar.button(":eyes:", on_click=search, args=(query,), type="primary")


primarycolor="#FF4B4B"
font="monospace"