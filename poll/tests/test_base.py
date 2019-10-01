from poll.models import Country

def create_some_countries():
    Country.objects.create(name="Afghanistan",name_official="Islamic Republic of Afghanistan",code2l="AF",code3l="AFG",flag_32="AF-32.png",flag_128="AF-128.png",latitude="33.98299275",longitude="66.39159363",zoom="6",)
    Country.objects.create(name="Aland Islands",name_official="Aland Islands",code2l="AX",code3l="ALA",flag_32="AX-32.png",flag_128="AX-128.png",latitude="60.25403213",longitude="20.35918350",zoom="9",)
    Country.objects.create(name="Albania",name_official="Republic of Albania",code2l="AL",code3l="ALB",flag_32="AL-32.png",flag_128="AL-128.png",latitude="41.00017358",longitude="19.87170014",zoom="7",)
    Country.objects.create(name="Algeria",name_official="People`s Democratic Republic of Algeria",code2l="DZ",code3l="DZA",flag_32="DZ-32.png",flag_128="DZ-128.png",latitude="27.89861690",longitude="3.19771194",zoom="5",)
    Country.objects.create(name="American Samoa",name_official="The United States Territory of American Samoa",code2l="AS",code3l="ASM",flag_32="AS-32.png",flag_128="AS-128.png",latitude="-14.30634641",longitude="-170.69501750",zoom="11",)
    Country.objects.create(name="Andorra",name_official="Principality of Andorra",code2l="AD",code3l="AND",flag_32="AD-32.png",flag_128="AD-128.png",latitude="42.54057088",longitude="1.55201340",zoom="11",)
