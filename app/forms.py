
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class pswForm(Form):

    email = StringField('Email', validators=[DataRequired()])
    idcard = StringField(
        label='身份证号',
        validators=[
            DataRequired(),
            Regexp(r'\d{18}', message='身份证号格式错误')
        ]
    )
    password = PasswordField('新密码', validators=[DataRequired()])
    confirm_password = PasswordField(
        label='确认密码',
        validators=[DataRequired(),
                    # 验证当前表单输入密码和password表单输入密码是否一致,如果不一致,报错
                    EqualTo('password', message='密码不一致')]
    )
    submit = SubmitField('更改密码')


class AdminLoginForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('LogAdmin')


class AdminForm(Form):
    name = StringField(
        label='管理员名称',
        validators=[DataRequired(message='不能为空'),
                    Length(3, 12, message='长度必须在3-12之间')])
    password = PasswordField(
        label='密码',
        validators=[DataRequired(),
                    Length(6, 16, message='密码格式不正确')])
    rights = SelectMultipleField(
        label='权限',
        validators=[DataRequired()],
        choices=[(1, "新闻"), (2, "病例"), (3, "管理管理员"), (4, "交通"), (5, "复工和人口"), (6, "物资")],
        coerce = int)

    submit = SubmitField(label='点击新建')


class RegistrationForm(Form):
    username = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空'),
                    Length(3, 12, message='用户名长度必须在3-12之间')]
    )
    password = PasswordField(
        label='密码',
        validators=[DataRequired(),
                    Length(6, 16, message='密码格式不正确，长度应在6-16之间')]
    )

    confirm_password = PasswordField(
        label='确认密码',
        validators=[DataRequired(),
                    # 验证当前表单输入密码和password表单输入密码是否一致,如果不一致,报错
                    EqualTo('password', message='密码不一致')]
    )
    name = StringField(
        label='真实姓名',
        validators=[DataRequired(message='不能为空'),
                    Length(2, 5, message='长度必须在2-5之间')]
    )
    idcard = StringField(
        label='身份证号',
        validators=[
            DataRequired(),
            Regexp(r'\d{18}', message='身份证号格式错误')
        ]
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired(),
            Email(message='邮箱格式错误')
        ]
    )
    phone = StringField(
        label='电话号码',
        validators=[
            DataRequired(),
            Regexp(r'1\d{10}', message='电话号码格式错误')
        ]
    )
    province = SelectField(
        label='省份',
        validators=[DataRequired()],
        choices=[
            ('11', '北京市'),
            ('12', '天津市'),
            ('13', '河北省'),
            ('14', '山西省'),
            ('15', '内蒙古自治区'),
            ('21', '辽宁省'),
            ('22', '吉林省'),
            ('23', '黑龙江省'),
            ('31', '上海市'),
            ('32', '江苏省'),
            ('33', '浙江省'),
            ('34', '安徽省'),
            ('35', '福建省'),
            ('36', '江西省'),
            ('37', '山东省'),
            ('41', '河南省'),
            ('42', '湖北省'),
            ('44', '湖南省'),
            ('44', '广东省'),
            ('45', '广西壮族自治区'),
            ('46', '海南省'),
            ('50', '重庆市'),
            ('51', '四川省'),
            ('52', '贵州省'),
            ('55', '云南省'),
            ('54', '西藏自治区'),
            ('61', '陕西省'),
            ('62', '甘肃省'),
            ('66', '青海省'),
            ('64', '宁夏回族自治区'),
            ('65', '新疆维吾尔自治区'),
            ('71', '台湾省'),
            ('81', '香港特别行政区'),
            ('82', '澳门特别行政区')
        ],
        default='33',

    )
    address = StringField(
        label='具体地址',
        validators=[DataRequired(),
                    Length(5, 80, message='地址必须为5-80字')]
    )

    submit = SubmitField(label='点击注册')
