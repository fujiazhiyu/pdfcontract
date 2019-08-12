# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from .contract import bp
from .forms import CommissionForm, ApplicationForm, InstructionForm, CommissionApplicationForm
from xpinyin import Pinyin
import time
from .util.number2CNmoney import CNmoney


def baseInfo(request):
    return {
        "email": request.form.get('email'),
        "student": request.form.get('student'),
        "district": request.form.get('district'),
        "subject": request.form.get('subject'),
        "degree": request.form.get('degree')
    }


@bp.route('/application', methods=["GET", "POST"])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        info = {
            "applyyear": request.form.get('applyyear'),
            "school": request.form.get('school'),
            "total": request.form.get('total'),
            "univalent": request.form.get('univalent')
        }
        info.update(baseInfo(request))
        generateCSS(info, "留学申请合同号： S-")
        return redirect(url_for('contract.application', contract_title=info["student"] + "-" + info["district"] + "留学申请合同.pdf"))
    return render_template('information.html', form=form)


@bp.route('/commission', methods=["GET", "POST"])
def commissioned():
    form = CommissionForm()
    if form.validate_on_submit():
        info = {
            "univalent": request.form.get('univalent'),
            "lesson": request.form.get('lesson'),
            "previous": request.form.get('previous'),
            "teacher": request.form.get('teacher'),
            "works": request.form.get('works')
        }
        info.update(baseInfo(request))
        generateCSS(info, "留学作品集辅导委托合同号： CT-")
        return redirect(url_for('contract.commission', contract_title=info["teacher"] + "老师-" + info["student"] + info["district"] + "留学作品集辅导委托合同.pdf"))
    return render_template('information.html', form=form)


@bp.route('/instruction', methods=["GET", "POST"])
def instruct():
    form = InstructionForm()
    if form.validate_on_submit():
        info = {
            "univalent": request.form.get('univalent'),
            "lesson": request.form.get('lesson'),
            "total": request.form.get('total'),
            "works": request.form.get('works')
        }
        info.update(baseInfo(request))
        generateCSS(info, "作品集指导咨询合同号： T-")
        return redirect(url_for('contract.instruction', contract_title=info["student"] + "-" + info["district"] + "作品集指导合同.pdf"))
    return render_template('information.html', form=form)


@bp.route('/commission-application', methods=["GET", "POST"])
def commissioned_apply():
    form = CommissionApplicationForm()
    if form.validate_on_submit():
        info = {
            "applyyear": request.form.get('applyyear'),
            "school": request.form.get('school'),
            "total": request.form.get('total'),
            "univalent": request.form.get('univalent'),
            "teacher": request.form.get('teacher')
        }
        info.update(baseInfo(request))
        generateCSS(info, "留学申请委托合同号： CS-")
        return redirect(url_for('contract.application_commission', contract_title=info["teacher"] + "老师-" + info["student"] + info["district"] + "留学申请委托合同.pdf"))
    return render_template('information.html', form=form)


def generateCSS(info, contract_prefix):
    with open('flaskr/static/userStyles.css', 'w') as fw:
        fw.write('''
            @media print {
                @page {
                    @top-left {
                        content: " ''' + contract_prefix
                 + time.strftime("%Y%m%d", time.localtime())
                 + "-" + Pinyin().get_pinyin(info["student"], '').upper() + '''";
                    }
                }

                .student-name::before {
                    content: " ''' + info["student"] + ''' "
                }

                .apply-district::before {
                    content: " ''' + info["district"] + ''' ";
                }

                .apply-subject::before {
                    content: " ''' + info["subject"] + ''' ";
                }

                .apply-degree::before {
                    content: " ''' + info["degree"] + ''' ";
                }
        ''')

        if "total" in info:
            if contract_prefix == "作品集指导咨询合同号： T-":
                total_money = str(int(info["total"]) - 100)
            elif contract_prefix == "留学申请委托合同号： CS-":
                fw.write('''
                    .previous-funds::before {
                        content: " ￥''' + str(int(info["total"]) - int(info["univalent"]) * (int(info["school"])-1)) + ''' ";
                    }
                ''')
                total_money = info["total"]
            else:
                total_money = info["total"]

            fw.write('''
                .total-amount::before {
                    content: " ''' + CNmoney().cwchange(total_money) + '(' + '￥' + total_money + ')' + ''' ";
                }
            ''')

        if "applyyear" in info:
            fw.write('''
                .apply-year-season::before {
                    content: " ''' + info["applyyear"] + '''年秋季 ";
                }
            ''')

        if "school" in info:
            fw.write('''
                .school-number::before {
                    content: " ''' + info["school"] + ''' ";
                }
            ''')

        if "univalent" in info:
            fw.write('''
                .univalent-amount::before {
                    content: " ''' + info["univalent"] + ''' ";
                }
            ''')

        if "lesson" in info:
            fw.write('''
                .instruct-lesson-hours::before {
                    content: " ''' + info["lesson"] + ''' ";
                }

                .half-lesson-hours::before {
                    content: " ''' + str(int(info["lesson"]) // 2) + ''' ";
                }
            ''')
            if "univalent" in info and "previous" in info:
                fw.write('''
                    .previous-funds::before {
                        content: " ''' + str(int(info["previous"]) * int(info["univalent"])) + ''' ";
                    }
                ''')

        if "works" in info:
            fw.write('''
                .works-number::before {
                    content: " ''' + info["works"] + ''' ";
                }
            ''')

        if "applyyear" in info:
            fw.write('''
                .fail-year::before {
                    content: " ''' + str(int(info["applyyear"]) + 1) + ''' ";
                }
            ''')

        if "teacher" in info:
            fw.write('''
                .teacher-name::after {
                    content: " ''' + info["teacher"] + '''";
                }
            ''')

        fw.write('''
            .sign-date::before {
                content: " ''' + time.strftime(" %Y 年 %m 月 %d 日", time.localtime()) + ''' ";
            }
        }
        ''')
