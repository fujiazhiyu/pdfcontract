# -*- coding: utf-8 -*-
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask, make_response
)
from flask_weasyprint import HTML, CSS, render_pdf
from urllib.parse import quote
from xpinyin import Pinyin
import os
import sys
import time
# from flask import current_app as app


bp = Blueprint('contract', __name__)


@bp.route('/', methods=['GET', 'POST'])
def onlinepreview():
    return redirect(url_for('contract.select'))


@bp.route('/contracttype', methods=['GET', 'POST'])
def select():
    return render_template('type-selection.html')


@bp.route('/application-contract/<contract_title>', methods=['GET', 'POST'])
def application(contract_title):
    html = render_template('application_contract.html')
    pdf_file = render_contract(html).write_pdf()
    return contract_response(pdf_file, contract_title)


@bp.route('/commission-contract/<contract_title>', methods=['GET', 'POST'])
def commission(contract_title):
    html = render_template('commissioned_contract.html')
    pdf_file = render_contract(html).write_pdf()
    return contract_response(pdf_file, contract_title)


@bp.route('/instruction-contract/<contract_title>', methods=['GET', 'POST'])
def instruction(contract_title):
    html = render_template('instruction_contract.html')
    instruction_document = render_contract(html)
    hygge_document = hygge_contract(contract_title)
    # 合并两个pdf 见：https://weasyprint.readthedocs.io/en/latest/api.html#weasyprint.document.Document.copy
    # 以及：https://stackoverflow.com/questions/38987854/django-and-weasyprint-merge-pdf
    all_pages = [p for doc in [instruction_document, hygge_document] for p in doc.pages]
    pdf_file = instruction_document.copy(all_pages).write_pdf()
    return contract_response(pdf_file, contract_title)


@bp.route('/application-commission-contract/<contract_title>', methods=['GET', 'POST'])
def application_commission(contract_title):
    html = render_template('application_commissioned_contract.html')
    pdf_file = render_contract(html).write_pdf()
    return contract_response(pdf_file, contract_title)


# 生成灰格教育咨询合同（单页那个）的css文件
def hygge_contract(contract_title):
    # 页眉和日期
    with open('flaskr/static/hyggeadd.css', 'w') as hygge_css:
        hygge_css.write("@media print { @page { @top-left { content: '咨询服务合同号： " + Pinyin().get_initials(contract_title.split("-")[0], '') + time.strftime(
            "%Y%m%d", time.localtime()) + "'}} " + ".sign-date::before { content: '" + time.strftime(" %Y 年 %m 月 %d 日", time.localtime()) + "'; }}")
    html = render_template('hygge_contract.html')
    cssfile = CSS(url_for("static", filename='hyggeadd.css'))
    return HTML(string=html).render(stylesheets=[cssfile])


def render_contract(html):
    userstylesheet_url = url_for("static", filename='userStyles.css')
    cssfile = CSS(url_for("static", filename="sample.css"))
    if os.path.exists("flaskr/" + userstylesheet_url):
        cssfile = CSS(userstylesheet_url)
    return HTML(string=html).render(stylesheets=[cssfile])


def contract_response(pdf_file, contract_title):
    # quote为url编码，这种写法也避免了safari下载中文文件名乱码
    http_response = make_response(pdf_file)
    http_response.headers["Content-Type"] = "application/octet-stream; charset=utf-8"
    http_response.headers['Content-Disposition'] = (
        "attachment; filename*=UTF-8''{}").format(quote(contract_title))
    return http_response
