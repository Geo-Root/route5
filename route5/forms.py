#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

from flask.ext import wtf
from flask.ext.wtf import Form
import wtforms
from wtforms.fields import TextField, BooleanField, PasswordField, TextAreaField, SelectField, HiddenField, FloatField, IntegerField
from wtforms import validators

GEO = {
    0: ("", ""),
    2004:("Afghanistan","AF"),
    2008:("Albania","AL"),
    2010:("Antarctica","AQ"),
    2012:("Algeria","DZ"),
    2016:("American Samoa","AS"),
    2020:("Andorra","AD"),
    2024:("Angola","AO"),
    2028:("Antigua and Barbuda","AG"),
    2031:("Azerbaijan","AZ"),
    2032:("Argentina","AR"),
    2036:("Australia","AU"),
    2040:("Austria","AT"),
    2044:("The Bahamas","BS"),
    2048:("Bahrain","BH"),
    2050:("Bangladesh","BD"),
    2051:("Armenia","AM"),
    2052:("Barbados","BB"),
    2056:("Belgium","BE"),
    2064:("Bhutan","BT"),
    2068:("Bolivia","BO"),
    2070:("Bosnia and Herzegovina","BA"),
    2072:("Botswana","BW"),
    2076:("Brazil","BR"),
    2084:("Belize","BZ"),
    2090:("Solomon Islands","SB"),
    2096:("Brunei","BN"),
    2100:("Bulgaria","BG"),
    2108:("Burundi","BI"),
    2112:("Belarus","BY"),
    2116:("Cambodia","KH"),
    2120:("Cameroon","CM"),
    2124:("Canada","CA"),
    2132:("Cape Verde","CV"),
    2140:("Central African Republic","CF"),
    2144:("Sri Lanka","LK"),
    2148:("Chad","TD"),
    2152:("Chile","CL"),
    2156:("China","CN"),
    2162:("Christmas Island","CX"),
    2166:("Cocos (Keeling) Islands","CC"),
    2170:("Colombia","CO"),
    2174:("Comoros","KM"),
    2178:("Congo","CG"),
    2180:("Congo","CD"),
    2184:("Cook Islands","CK"),
    2188:("Costa Rica","CR"),
    2191:("Croatia","HR"),
    2196:("Cyprus","CY"),
    2203:("Czech Republic","CZ"),
    2204:("Benin","BJ"),
    2208:("Denmark","DK"),
    2212:("Dominica","DM"),
    2214:("Dominican Republic","DO"),
    2218:("Ecuador","EC"),
    2222:("El Salvador","SV"),
    2226:("Equatorial Guinea","GQ"),
    2231:("Ethiopia","ET"),
    2232:("Eritrea","ER"),
    2233:("Estonia","EE"),
    # 2239:("South Georgia and the South Sandwich Islands","GS"),
    2242:("Fiji","FJ"),
    2246:("Finland","FI"),
    2250:("France","FR"),
    2258:("French Polynesia","PF"),
    2260:("French Southern and Antarctic Lands","TF"),
    2262:("Djibouti","DJ"),
    2266:("Gabon","GA"),
    2268:("Georgia","GE"),
    2270:("The Gambia","GM"),
    2276:("Germany","DE"),
    2288:("Ghana","GH"),
    2296:("Kiribati","KI"),
    2300:("Greece","GR"),
    2308:("Grenada","GD"),
    2316:("Guam","GU"),
    2320:("Guatemala","GT"),
    2324:("Guinea","GN"),
    2328:("Guyana","GY"),
    2332:("Haiti","HT"),
    2334:("Heard Island and McDonald Islands","HM"),
    2336:("Vatican City","VA"),
    2340:("Honduras","HN"),
    2348:("Hungary","HU"),
    2352:("Iceland","IS"),
    2356:("India","IN"),
    2360:("Indonesia","ID"),
    2368:("Iraq","IQ"),
    2372:("Ireland","IE"),
    2376:("Israel","IL"),
    2380:("Italy","IT"),
    2384:("Cote d'Ivoire","CI"),
    2388:("Jamaica","JM"),
    2392:("Japan","JP"),
    2398:("Kazakhstan","KZ"),
    2400:("Jordan","JO"),
    2404:("Kenya","KE"),
    2410:("South Korea","KR"),
    2414:("Kuwait","KW"),
    2417:("Kyrgyzstan","KG"),
    2418:("Laos","LA"),
    2422:("Lebanon","LB"),
    2426:("Lesotho","LS"),
    2428:("Latvia","LV"),
    2430:("Liberia","LR"),
    2434:("Libya","LY"),
    2438:("Liechtenstein","LI"),
    2440:("Lithuania","LT"),
    2442:("Luxembourg","LU"),
    2450:("Madagascar","MG"),
    2454:("Malawi","MW"),
    2458:("Malaysia","MY"),
    2462:("Maldives","MV"),
    2466:("Mali","ML"),
    2470:("Malta","MT"),
    2478:("Mauritania","MR"),
    2480:("Mauritius","MU"),
    2484:("Mexico","MX"),
    2492:("Monaco","MC"),
    2496:("Mongolia","MN"),
    2498:("Moldova","MD"),
    2499:("Montenegro","ME"),
    2504:("Morocco","MA"),
    2508:("Mozambique","MZ"),
    2512:("Oman","OM"),
    2516:("Namibia","NA"),
    2520:("Nauru","NR"),
    2524:("Nepal","NP"),
    2528:("Netherlands","NL"),
    2540:("New Caledonia","NC"),
    2548:("Vanuatu","VU"),
    2554:("New Zealand","NZ"),
    2558:("Nicaragua","NI"),
    2562:("Niger","NE"),
    2566:("Nigeria","NG"),
    2570:("Niue","NU"),
    2574:("Norfolk Island","NF"),
    2578:("Norway","NO"),
    2580:("Northern Mariana Islands","MP"),
    2581:("US Minor Outlying Islands","UM"),
    2583:("Micronesia","FM"),
    2584:("Marshall Islands","MH"),
    2585:("Palau","PW"),
    2586:("Pakistan","PK"),
    2591:("Panama","PA"),
    2598:("Papua New Guinea","PG"),
    2600:("Paraguay","PY"),
    2604:("Peru","PE"),
    2608:("Philippines","PH"),
    2612:("Pitcairn Islands","PN"),
    2616:("Poland","PL"),
    2620:("Portugal","PT"),
    2624:("Guinea-Bissau","GW"),
    2626:("East Timor","TL"),
    2634:("Qatar","QA"),
    2642:("Romania","RO"),
    2643:("Russia","RU"),
    2646:("Rwanda","RW"),
    2654:("St. Helena","SH"),
    2659:("St. Kitts and Nevis","KN"),
    2662:("St. Lucia","LC"),
    2666:("St. Pierre and Miquelon","PM"),
    2670:("St. Vincent and the Gren.","VC"),
    2674:("San Marino","SM"),
    2678:("Sao Tome and Principe","ST"),
    2682:("Saudi Arabia","SA"),
    2686:("Senegal","SN"),
    2688:("Serbia","RS"),
    2690:("Seychelles","SC"),
    2694:("Sierra Leone","SL"),
    2702:("Singapore","SG"),
    2703:("Slovakia","SK"),
    2704:("Vietnam","VN"),
    2705:("Slovenia","SI"),
    2706:("Somalia","SO"),
    2710:("South Africa","ZA"),
    2716:("Zimbabwe","ZW"),
    2724:("Spain","ES"),
    2740:("Suriname","SR"),
    2748:("Swaziland","SZ"),
    2752:("Sweden","SE"),
    2756:("Switzerland","CH"),
    2762:("Tajikistan","TJ"),
    2764:("Thailand","TH"),
    2768:("Togo","TG"),
    2772:("Tokelau","TK"),
    2776:("Tonga","TO"),
    2780:("Trinidad and Tobago","TT"),
    2784:("United Arab Emirates","AE"),
    2788:("Tunisia","TN"),
    2792:("Turkey","TR"),
    2795:("Turkmenistan","TM"),
    2798:("Tuvalu","TV"),
    2800:("Uganda","UG"),
    2804:("Ukraine","UA"),
    2807:("Macedonia (FYROM)","MK"),
    2818:("Egypt","EG"),
    2826:("United Kingdom","GB"),
    2834:("Tanzania","TZ"),
    2840:("United States","US"),
    2854:("Burkina Faso","BF"),
    2858:("Uruguay","UY"),
    2860:("Uzbekistan","UZ"),
    2862:("Venezuela","VE"),
    2876:("Wallis and Futuna","WF"),
    2882:("Samoa","WS"),
    2887:("Yemen","YE"),
    2894:("Zambia","ZM"),
}

geo_keys = []
for k,v in GEO.items():
    geo_keys.append([ str(k), v[0] ])
geo_keys.sort(key=lambda x: x[1])

class LoginForm(Form):
    
    user_username = TextField(label="Username", validators=[validators.Required(), validators.Length(min=4, max=25)])
    user_password = PasswordField(label="Password", validators=[validators.Required()])


class UserForm(Form):

    user_name = TextField(label="First name", validators=[validators.optional()])
    user_lastname = TextField(label="Last name", validators=[validators.optional()])
    user_country = TextField(label="Country", validators=[validators.Optional()])
    user_mobile = TextField(label="Mobile number", validators=[validators.Required()])
    user_country = SelectField("Country", default="2840", choices=geo_keys, option_widget=wtforms.widgets.Select(multiple=True))
    user_language = SelectField(label="Language", choices=[("Eng", "English")], default=("Eng", "English"), validators=[validators.optional()])
    user_code5 = HiddenField(label="Code5", validators=[]) # TODO: add custom validator for code5
    user_promotion_code = TextField(label="Promotion", validators=[validators.optional()])


class RegisterForm(UserForm):

    user_email = TextField(label="Email", validators=[validators.Required(), wtforms.validators.Email()])
    user_username = TextField(label="Username", validators=[validators.Regexp(r'^[\w]+$'), validators.Required(), validators.Length(min=4, max=25)])
    user_password1 = PasswordField(label="Password", validators=[validators.Required(), validators.Length(min=3)])
    user_password2 = PasswordField(label="Repeat password", validators=[validators.Required(),  validators.EqualTo('user_password1', message='Passwords must match')])


    def validate_user_code5(self, field):
        pass

    def generate_code5(self):
        pass


class UserRegisterForm(RegisterForm):
    pass


class ShipperRegisterForm(RegisterForm):
    pass


class BusinessRegisterForm(RegisterForm):
    pass


class AdminRegisterForm(RegisterForm):
    pass


class PromotionCodeForm(Form):

    promotion_code = None


class ShipmentForm(Form):

    sh_user = TextField(label="Username", validators=[validators.Regexp(r'^[\w]+$'), validators.Required(), validators.Length(min=4, max=25)])
    sh_weight = FloatField(label="Weight")
    sh_status = TextField()
    sh_code5 = IntegerField()
    sh_tracking_number = IntegerField()

