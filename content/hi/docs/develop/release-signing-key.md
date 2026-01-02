---
title: "रिलीज़ साइनिंग की (Release Signing Key)"
description: "I2P रिलीज़ को साइन करने के लिए उपयोग की जाने वाली PGP कुंजियाँ और उन्हें कहाँ से प्राप्त करें"
slug: "release-signing-key"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

<p> रिलीज़ 0.9.57 और आगे की सभी रिलीज़ idk द्वारा साइन की गई हैं। उनकी वर्तमान public key है: </p> <p> <a href="/idk.key.asc" >PGP public key डाउनलोड करें</a> </p><p>

<p> रिलीज़ 0.7.6 और 0.9.56 zzz द्वारा हस्ताक्षरित हैं। उनकी वर्तमान सार्वजनिक कुंजी है: </p> <p> <a href="/zzz.key.asc" >PGP सार्वजनिक कुंजी डाउनलोड करें</a> </p> <p> <pre> -----BEGIN PGP SIGNED MESSAGE----- Hash: SHA1

मैंने नई GPG keys और subkeys बनाई हैं और पुरानी key से नई keys को sign किया है।

पुरानी कुंजियाँ:

	pub   1024D/A76E0BED 2005-12-16
	      Key fingerprint = 4456 EBBE C805 63FE 57E6  B310 4155 76BA A76E 0BED
	uid                  zzz (zzz) <zzz@mail.i2p>
	sub   2048g/74C8122D 2005-12-16

नई कुंजियाँ:

	pub   4096R/EE7256A8 2014-05-08 [expires: 2024-05-05]
	      Key fingerprint = 2D3D 2D03 910C 6504 C121  0C65 EE60 C0C8 EE72 56A8
	uid                  zzz on i2p (key signing) <zzz@mail.i2p>
	uid                  zzz on i2p (key signing) <zzz@i2pmail.org>
	sub   4096R/1AE988AB 2014-05-08 [expires: 2019-05-07]
	sub   4096R/01B5610C 2014-05-08 [expires: 2019-05-07]
	sub   4096R/59683006 2014-05-08 [expires: 2019-05-07]

मैं नई keys का उपयोग निम्नानुसार करूंगा:

	EE7256A8: key signing
	1AE988AB: email signing
	01B5610C  email encryption
	59683006  release signing

रिलीज़ साइनिंग की (release signing key) का उपयोग 0.9.13 रिलीज़ से शुरू किया जाएगा। यह संदेश मेरी पुरानी की (key) के साथ साइन किया गया है।

zzz 25 मई, 2014

नई कुंजियाँ इस प्रकार हैं:

- -----BEGIN PGP PUBLIC KEY BLOCK-----

Version: GnuPG v1.4.14 (GNU/Linux)

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 kHp

iEYEARECAAYFAlOB3xkACgkQQVV2uqduC+3+UgCfYZiUtx7FDGdQDhdVP8MyRf0D ANIAn2YHOQh4yv84u2Kuars1gC0j3Nr2 =Zu9F -----END PGP SIGNATURE----- </pre>

<p> 0.9.9 से जारी किए गए संस्करणों पर str4d द्वारा हस्ताक्षर किए जा सकते थे। उनकी वर्तमान सार्वजनिक कुंजी है: </p> <pre> -----BEGIN PGP SIGNED MESSAGE----- Hash: SHA512

मेरी वर्तमान सार्वजनिक कुंजियाँ निम्नलिखित हैं:

pub   4096R/0EC51FCDA94FB53E 2014-03-11 [समाप्त होता है: 2019-03-10] uid               [  पूर्ण  ] str4d (http://str4d.i2p) <str4d@mail.i2p> uid               [  पूर्ण  ] str4d <str4d@i2pmail.org> sub   4096R/1CC61D9B33C3241B 2014-03-11 [समाप्त हो गया: 2015-03-11] sub   4096R/803DEE491A3473E7 2014-03-12 [समाप्त हो गया: 2015-03-12] sub   4096R/A1B84C9B733AAC82 2015-04-05 [समाप्त होता है: 2016-04-04] sub   4096R/13B5EE58C09FB3E0 2015-04-05 [समाप्त होता है: 2016-04-04]

मैं वर्तमान में keys का उपयोग निम्नानुसार करता हूं:

        A94FB53E: key signing
        733AAC82: email encryption
        C09FB3E0: email and release signing

मैं प्रतिवर्ष नई encryption और signing subkeys उत्पन्न करता हूं। मेरे द्वारा हस्ताक्षरित कोई भी I2P release हमेशा रिलीज़ के समय नवीनतम signing subkey के साथ हस्ताक्षरित होगा।

str4d Nov 20, 2015

वर्तमान keys (उपरोक्त तारीख के अनुसार) निम्नलिखित हैं:

- -----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBFMfofkBEADlyw6v1hGBtnIISujt/18RJcVTLAxYtfe3DsGhWqYZN3iKGGWb NJ5vZcV65FVH/70NFnmKlvYp+tVNJcoRtEYpfwiNG7nIyOC4GgaSLwkNVgLcFZhV mNj2RIJphjN5qsWm6ut9p9CyhWkVNJYDP65gqwShZQ2lPboo9s0XjUF78SrSshy2 iVij0xu6oqdjwqn1B7L3lXVYCwxReCvSdFnBMpjGUEgGnbt7euhrViFk8FrUkAje 2tZA5FAUA/t2Mnc9JREe6WlbZ44mLApOjFdw0g415FdcnS2GGaYuXNG1lJ1yOA33 n9JXT7A31wPyiw5yz7fxgl7ZNYZr2TsRjBlqEhf2SCPfqU9UlhJ9NqApaPyCEr+8 oZQfZ9r6stc98MlnmdQ7p4SmKRwCLiBtgmrB8mbgYV+iOwaKztqEoma3FoO2EJ+j Gx+UrJ0bIFVr6sL0ulfneYlY76wWWRpB/pLLgIMmZw83uB+JDBQyZFXcAHj9jMQ7 ZNn0MNQ/I+qcmX+CRAyl2+cQHUVbbQWDjB3crZlpK5TGw/x7w0YxBYAH8Us5JqJH QOsact8ADnE4IiKm5gVefFmNX6vsljkNESdpAMxnB7Ckl2XV/r5sKwrdxxUbFSxp IKGx2uKGUs4oUffOzpKULhGBWypN+3fVwvP+q896Il9hgyx6SCQ8AgPHRwARAQAB tClzdHI0ZCAoaHR0cDovL3N0cjRkLmkycCkgPHN0cjRkQG1haWwuaTJwPokCQAQT AQoAKgIbAwUJCWYBgAULCgkIBwYVCgkIAwIEFgMCAQIeAQIXgAUCUx/ZQgIZAQAK CRAOxR/NqU+1Pk9EEADHdpsmrA6ZKU4EmBZNbw62D7tAo00Fh25m8OuIkXtOqEbF /guTZiZM4nbhZpPFG9sCN1bXS8VslA7isOedbznkKnSK0BJcrzldwKzW25cwptoQ CCqTUarYbhcIzEOKNetYqICWrVTy2Yuc37maA66PnRLphV7pP3Fj7eN6aMtqwtpJ YukIU4LAjKOMJ6gwy7tjsZYbAqgSE8wRJm7i1MfO1W864a1l2a68Gooz03NC6mfY J8aW0y1F87xMJIgZeN7OyHf2AC4/Tp/cL+Gd3HcUuoRjmWBgaxH8tVNgfxSIUMNH 5pTdDs5VlRolwlOEcTW5VxOSu5C7ZbuKyFmbI0DSevDVGS0rxSSizjlyGmnxkLU1 ozpeIwTbwTUzvd26+k8cidGodKqoNoyAXzjaiBXYKgIrVeXBMHxCGeQtGeEhQR+L OXs8cEX6xpt9g7nKbNki0Cfv/lx9Byn+0v9RvMJKDa1mOSKbNOx3NJ8+ewdTVkTs iYFTZwpJexbfovPYqTdisiO7dv0i5teE8sEj25icdPtKYvn/55JCT67E8MVZaeyU YOaMPtgsiOX0v68NtrC1L37UuBykQlm7FdobN4Sg5FnLTt4IWktf0/vsaLdhRozD KsbTmsumCrScAwZfa0H3S8WqK6yCEKjPi+J4xG1OZP1WptlV41wLnFKkeFaZRIkB HAQTAQoABgUCUx/Y+AAKCRDV3jiWlKRlsmU0B/96eiPHIIvapoXKoZSt23OFjXG+ 3xp/Zzf2Ug0384FYZJ1eX/R2IWsh64CVvOR0LMFvHvPU7SCMu2OreNHfPx/B/kn8 MmusGy6JHP25A4BWzs1eeyKgYQTFz7vSCeAnytmcdBot1s099upIRw4usCLhdxzv Qyx6TogAacGC3YFj7o0agz+ApPnCQZ68kZpDOCDrtOe/DRted1LLXM661Cp15d5R d+91ZSKfQ9xjK1d2k8iMYJqWYll50DalGtzPGDB335gX7agliI5dYiu2XSLyynhw /7f8d0Bz8KVj7pgCroAVjTSdHvZfVcZJU4HST/jHx5hilVUzkr9NK5YONJ8SiQQc BBABCgAGBQJTKlm2AAoJEPvivaOtdGgqmGAgALl0eAcUSF7IuloPT4VyJeNGMuOb 7aN4yYrGBM+y7Ij/dTWSS1yjlcixsqd+s0dqGse6RtJkyhkisEmNdS7Sf62okGDl ZbmhjvMQteUO1zw+CREdfx5oMpW/eCHq/Pzw8KRdp6qY0wBRj10GFMAaMX8XCNOh 6B6Ti0AQ/424yEvcPpA0zXwvLGylFozRxjK6qWEHEmW/+knxYYN/W+8TERuwVJSN F3jBYl73DTVBZ4bzpu5jMSydhRD02nV2LbnolhbCzGllLkhQw6iFW36br8600Tba loQhcJU+cmuCId/B6xXcF+fyWqmMmm+b0UFoHGRBnXCf4gBcjCK0UwJ1lUOTY5qg IYJTrBpCrGAoGTd9s+1CtnnZFlIcwFJB7NwMZEsTWvOvO6sZPYP33ktcUwWAKqNj 3sSjy43kdfUeVip0jzV0K5uStC+DiVq8VwH7uNIH2UbkQZato67WgShUCCaSvf2p HapSRdrmwIaoANQuEluhytdafX7yqJXGkhYI0Ylh2FH3oZyTnz1XoB5y5T1OpFpi I7CgjRO677aieRsf6HACHPX5mWcq8zJQ8fuxoHZ5GJ8FEyk6ULUgFJ3u9SgG5k5I vP4pK8+lP/d90Zf98Uaq4aMgAoIlrtwz68Bv/KUlpwVWhiIgo89C5UwcTUNQOmi3 0PxCpamM81NwGPxjZAqr/+0YP3NBtJOITL0oqRCxcHCJ9N8gmqUmUEgEffP+glsJ p/mQeJEacmR9loz6WAB6GT9mu5TvX6bZ5EawnluQ1mI6Tn+v6ltjhKzPzaVhOo6d iKriQFZhcelX1qDnE3zs7driBeacuKGt4URV8A+UDGJBeIAEfrlszor3FQ0qOUPs plbcbB4YudUOhlH1REtGx7zWVFefuy80ZC7abHsPhWkJow2axWlvPqjSsd/KgpjG IAHIZxiYAozNJqDNluGx1+qa1d7/YINthZKefhkG3XDLuhgxvD8rAovyAFW/8Vy0 S+GpzUVtC8HY9FZf2gRkVtZQGboZck2uFyIaU/Ni4ahX8Z9IvtsU9JPLzp0HRgAv 9kz9EyRZt1viueeIVcmadHirUe1IKqndeslcXOX4dUF0nrqP1+shYhebgq93rMPR yH3EsoXtAP1KCN8tWPdnlDnMY0Zpy32mfCL0hMMnH+CY5rARssSbiFP9HeWk/CN+ yES7FY705QmV/2SV4rEngqnIcrcqEJFp49JPihC1pSikHCItzSVFaODbUl4qhTjn Tjtl0pdFQc9ksA/6IEOH/bufDwtxCLwAjUpqyNGEH/8FnxtwotsTmhmTWMe9vxYe YStdTLkAvJFMVEU0W+H2ZZG481P5/8tqFS9cHEU++3VvuYxfipwjpIQhm5WJARwE EAEKAAYFAlMuEVwACgkQq+DDGd8KChpPGwf/QL66k12OzqI40KQL+UbzW25vxbmE OyZ1MT9SuUVt6Th9zdoNm9Cosi9kOiq+DPLFFT751Lmm1hcM0rDDNeN+l8wpLwX9 EifD/bQ7Q5esM8NJmGVyhA/Cd3wkp5yYNdZPOu9/0xpe/Px4YgficRErhgyVh2Vs svQRQ0WcTYbgbmQFpOUsjNVOchJMFERSJaQxWgN3olYd5DTDxPDLztt3vdBCIkz0 4OAotZqbqdnmvlkjKjzrJylfCkyo9bOU471v6Hs3mfUQXo9nXC9zGETFWsvB4WCC QdWEyj+2K+PcdZU0FEPonfTouVcsR9oTqQqqfg21M7HUHSmlrOyCLqNnZ4kCHAQQ AQIABgUCU2vk5AAKCRDuYMDI7nJWqGIzD/9vdI3uUUYGCaURAprGEo4kk6JP2TcS AmyO9Pr8bBdpmt/DVFK0zWllQ+69QAWLFoCmgjOgWUPRNWA+ldG5lzExjuuP38P1 4HupPMh0yOd+QUod4Gdi+hqPCuFT4/oErWZcOGGXAw4ZcvdEGKY9E975D+3yd7sG HGskvGB/UmLIBQ2XfQOoqk0A9eXz55wLN1ia1imHd/0NkPkQOHkjTdOtHhcBhuoc ttex9HcmYy2g5oorG+7wx0EtHxIhuCcRq1wQgXm2JtbiFHXiH0MpLfBr29kpzH7y 8jompGgAJsK8uRwTC8UFWHnx0VxnFQ+4vinqlgj7/O+WMZ/siDlOZDo2RC3ts+Ct 91kYNFHsycrkJYuoPzNcMy7mmixQFj5L2VIG1Ne3OTdEPVWE5jIQ/w5IX0aYxNt4 ANIZJA/r1AqDqDEhto6gdnkrVZSJN+Mvd7yj7XTbrErpTmQeNkGgb9ult4XaEOdm bjAjE6rTQqFD3Tn8SeXNgkJFr0Zb8lZypmOL6cxU4vTG66blJPLZGuaH3yCrtA1i ynZPrV2TYiET+fhg2TBEXbjLkWHQnA+7sFFOTgK5WOqc6vK29h5ssEQKIFodDh4a e88tiGLW9lSc+YWRpKHgEc8QDXIuBrV18hZEvbITvLZnnf5uIFXJV5ZCHG+o6I+Y jQrPY4oC2HGrMIkBIgQQAQoADAUCVRRYygWDB4YfgAAKCRCFZ1M6Yr7+XbxwB/42 Kbk6DpZueEK0qtdoLUh7H+dWfwA0Gsh/vCoS6RM9iXjKPBoQGlbCBpsBpqCJkGd/ iXH+tnkU2dq4BvGc/igSHadNYmYq077l1vu3pJjDjxfQ2qZSF9D27EUzlXLd4Q6s hysZ18HoTehxr3AG33N1tEm9kBUfZjeMZxk7zbty3Lo7tK/UYN+4mIgYqLc97XIe 40Z

iQIcBAEBCgAGBQJWT6iBAAoJEBO17ljAn7PgnxIP/RevbXaCm2Q3ildI0YLjQFDr vSIGKsCjD9nZY3ETk+CNFGOL4aYWp96HWuQoMq7B6qlb/sLejN/Ssu3M0sxf2hNK pCIagZClqRchSBK+0UpAEIs98sf0sPakqKg0FlOJhuCsKHMUOxpQJ4qCDh6f24b2 cqKR8GjyUAgSeiiyN+DkDyqRYingQGAU5vzKepYzX+DMHC/izqQhrwQLVImv20wr 5pKZJDjfOpYUZRTuScV5Qwcgc0JYcMOjfgA93ZUA2zDrGIpw3dcCSMrpNQcvM6Cg 1mfiLZzkvPH3UkUOWhHCn/N2XaAF58joCaS+/bVUaXx02IbxJ1TTjqtCiH9491mE aaHeRCFYbkKCXWjuxCx1+VZN2yRk24rSkis/+LFgZm850fXgYfrqiyPRDlCMApdo 5JDUBTioyZz24vhqWpe0OZueu11DXtpU1G0BiheGrweXAAx0Yki8dRiPTXkavAMj oMBND9G7a1564KOe+t6V2qUyH50+3NaANvIiDJZbspX7yl8eVzPbwcGvtHzmHdnV pDh+38XUQEID5YJ/mdZh6evzmmTnQR1HVqPVrzs8SwIDO++tqj8DXTjID47c3VIl YhCMNlucciFxVn/sYI5qiJzCEMLMbvG+EhnoLNU4JGjfzo6I0RCpPfbrDfOsWJNi zYMz9htqusCQsGwUZSTZ =XBC5 -----END PGP SIGNATURE----- </pre>

<p> str4d ने निम्नलिखित रिलीज़ पर हस्ताक्षर किए हैं: </p> <ul> <li>0.9.23</li> </ul>

<p> रिलीज़ 0.7.6 से 0.9.12 तक zzz द्वारा निम्नलिखित कुंजी के साथ हस्ताक्षरित किए गए थे: </p> <p> <pre> -----BEGIN PGP PUBLIC KEY BLOCK----- Version: GnuPG v1.4.6 (GNU/Linux)

mQGiBEOjTnURBADegKKrIP6pz4+n57dqo3l9QrKhIklCtIxgJkL06ZJq5fKAnMLv GPaGXmn5vRrbo6QzHs/lGLG+ySWFWr9SsVstNKrwk+F1yGIERutl0BqMwX1esfN2 ugiZ3wB1yRu0PIrkm5cuDAFASFE+2lBjr1lfOrhw/dV+lLTcWx4NzkMzlwCgxgIk 4cqQMGaVkmtuICQdYmmMicUD/AmNSVJEm2XUvaS5fYWsHJG3+oNkdNGcx5SOMUdk PFwcSozqvT9FeIP76OVHAshQKeftE3utOFANQ/YomXEnypmwMxLLR+GPw5pMbKlK 6p+87aJZz+SA95E3ekmh7MmndvRd5RJDboUZy2H0FKX+FgaBlpsLl0uhT6uDuM/s 7nb0A/9nEAgICOU5SeXtO3jKY+RQvKyE0AblK7xVaU+Sn8ly0zauOJD13rycVGhu vLcAUVR3FKEjxafpvZ0ZPBo7AACjSDqAoCw/s/vt9gmrhHKiqN31PhYYLhKdfKTs 4LzWKTWKIAOwErkbYsMAXWKFT3LXsrEYvxq5j5m/6zMOwz2N7rQYenp6ICh6enpA IDx6enpAbWFpbC5pMnA+iF8EExECAB8FAkOjTnUCGwMGCwkIBwMCBBUCCAMDFgIB Ah4BAheAAAoJEEFVdrqnbgvtxGsAn39SvQ3+ey87WDDG+TWArN6oU8gnAJ4zeAsA LUK37WZIt8OImZSxk37uQbkCDQRDo06VEAgAy2UeqsM5a+U6ZOWS9NQiILb3KbTL FeeAd2rn9oLSLpn5gDWycwUS0Q62JmbSMWy6m9aczpnxvwaBYXz6aCIvZmTNtaU6 vyR/6wfJDyiUWSHtCyjpyFFYJimANd8Y8dDCimvceI/ihEDVyBX0kkgUGRAn8t3e unaLXqhbfiLiFw/GG1MNxUMzHt55/+9AqLOfRZg0riZvDoV79K+1sYSs8n1WeaVc T3wTb+Cb7fKNN7GT1MUhcXIoYYY6FGwsy5EWFsxYBRervqHtBJog2SoNUa/6BFGr zX+LDjK9L3xMTr3+fHIt4gPR/Lt4nnfEzL+rjClz/Fazmv38BRwPuKahFwADBQgA nD/AvZCnbWSB6khAVMqva5ROaD0gV0/UejCelZdYfgfHeCmrcMNQ+wCyww2NPsih 9vB1w+AUE0pdH37k65VZN+2falUdzN+PFugJGuH2pmlVOprH2SuC5gKpGRvzUqV5 U0nJmT2okDpW/52asUDJJLu1g//A3qBP83WGvSKUZg/ZisZA0qTiHH4QpjklopXi sSxR2hT8Fr9gF9WmDa09wbxE2xh/EL7gvVg/vk0gwOJcsFd67bNC+KUMOnjhOP0T K0/Ah4TEEs/hHNe9RsyyWlMoIUsF8AhG71ISOrJ5lLSXNe151XEb5FzZRM8sD9Zq 0E3PjmLbdVhanYvsPnWK6YhJBBgRAgAJBQJDo06VAhsMAAoJEEFVdrqnbgvtXTwA njMu9ueCFbsjme7nwsz96PdazJcHAKCce17hGI25QNXDZyHohrjha6IxDg== =fAfi -----END PGP PUBLIC KEY BLOCK-----

</pre> <p> रिलीज़ 0.6.1.31 से 0.7.5 तक Complication द्वारा हस्ताक्षरित किए गए थे। उनकी सार्वजनिक कुंजी है: </p> <p> <pre> -----BEGIN PGP SIGNED MESSAGE----- Hash: SHA1

नमस्ते,

मैं प्रमाणित करता हूं कि नीचे मेरी नई सार्वजनिक कुंजी है, जो 2007-11-24 को जारी की गई है, 2009-11-23 तक वैध है, और इसका कुंजी फिंगरप्रिंट है:

73CF 2862 87A7 E7D2 19FF DB66 FA1D FC6B 79FC CE33

यदि आपके पास मेरी पुरानी सार्वजनिक कुंजी है, और इसे सत्यापित करने के लिए इसका उपयोग करते हैं, तो आप देखेंगे कि मेरी पुरानी कुंजी 2007-11-15 को समाप्त हो गई थी। इस अपडेट में देरी के लिए क्षमा चाहता हूँ।

जो लोग इस संदेश से सीधे key को कॉपी करना चाहते हैं, लेकिन इसे e-mail प्रोग्राम का उपयोग करके नहीं पढ़ रहे हैं, कृपया याद रखें कि public key block के शुरुआत और अंत marker से "- " escape sequences को हटा दें। अन्यथा इसे पहचाना नहीं जाएगा।

जटिलता।

- -----BEGIN PGP PUBLIC KEY BLOCK-----

Version: GnuPG v1.4.7 (GNU/Linux)

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 z4Ja+hJ3dgCeL3mqvOEHG7AcUQrSlc6xlC1vbNY= =rGxK - -----END PGP PUBLIC KEY BLOCK----- -----BEGIN PGP SIGNATURE----- Version: GnuPG v1.4.7 (GNU/Linux)

iD8DBQFHR/zm4tLxqYRsGn0RAtCfAJ9rz+tsyEbeUAHcogdzgSPfuiWOAwCfWaVn Aiib6V5wOPbYTy13ADmxhfE= =mPFq -----END PGP SIGNATURE----- </pre>
