def stockhoka(data, partition_key):
    data2 = data.split('^')  

    recvvalue = []
    a=0
    for i in data2:
        a+=1
        if a == 3:
            recvvalue.append(i)
        else:
            recvvalue.append(float(i))

    fields = {
        "MKSC_SHRN_ISCD": recvvalue[1],
        "HOUR_CLS_CODE": recvvalue[2],
        **{f"ASKP{i+1}": recvvalue[i+3] for i in range(10)},
        **{f"BIDP{i+1}": recvvalue[i+13] for i in range(10)},
        **{f"ASKP_RSQN{i+1}": recvvalue[i+23] for i in range(10)},
        **{f"BIDP_RSQN{i+1}": recvvalue[i+33] for i in range(10)},
        "TOTAL_ASKP_RSQN": recvvalue[43],
        "TOTAL_BIDP_RSQN": recvvalue[44],
        "OVTM_TOTAL_ASKP_RSQN": recvvalue[45],
        "OVTM_TOTAL_BIDP_RSQN": recvvalue[46],
        "ANTC_CNPR": recvvalue[47],
        "ANTC_CNQN": recvvalue[48],
        "ANTC_VOL": recvvalue[49],
        "ANTC_CNTG_VRSS": recvvalue[50],
        "ANTC_CNTG_VRSS_SIGN": recvvalue[51],
        "ANTC_CNTG_PRDY_CTRT": recvvalue[52],
        "ACML_VOL": recvvalue[53],
        "TOTAL_ASKP_RSQN_ICDC": recvvalue[54],
        "TOTAL_BIDP_RSQN_ICDC": recvvalue[55],
        "OVTM_TOTAL_ASKP_ICDC": recvvalue[56],
        "OVTM_TOTAL_BIDP_ICDC": recvvalue[57],
        "STCK_DEAL_CLS_CODE": recvvalue[58]
    }

    return fields

def stockspurchase(data_cnt, data, partition_key):
    menulist = "MKSC_SHRN_ISCD|STCK_CNTG_HOUR|STCK_PRPR|PRDY_VRSS_SIGN|PRDY_VRSS|PRDY_CTRT|WGHN_AVRG_STCK_PRC|STCK_OPRC|STCK_HGPR|STCK_LWPR|ASKP1|BIDP1|CNTG_VOL|ACML_VOL|ACML_TR_PBMN|SELN_CNTG_CSNU|SHNU_CNTG_CSNU|NTBY_CNTG_CSNU|CTTR|SELN_CNTG_SMTN|SHNU_CNTG_SMTN|CCLD_DVSN|SHNU_RATE|PRDY_VOL_VRSS_ACML_VOL_RATE|OPRC_HOUR|OPRC_VRSS_PRPR_SIGN|OPRC_VRSS_PRPR|HGPR_HOUR|HGPR_VRSS_PRPR_SIGN|HGPR_VRSS_PRPR|LWPR_HOUR|LWPR_VRSS_PRPR_SIGN|LWPR_VRSS_PRPR|BSOP_DATE|NEW_MKOP_CLS_CODE|TRHT_YN|ASKP_RSQN1|BIDP_RSQN1|TOTAL_ASKP_RSQN|TOTAL_BIDP_RSQN|VOL_TNRT|PRDY_SMNS_HOUR_ACML_VOL|PRDY_SMNS_HOUR_ACML_VOL_RATE|HOUR_CLS_CODE|MRKT_TRTM_CLS_CODE|VI_STND_PRC"
    menustr = menulist.split('|')
    recvvalue = data.split('^')

    i = 0
    fields = {}
    for cnt in range(data_cnt):     
        for menu in menustr:
            if menu in ["HOUR_CLS_CODE","TRHT_YN","MRKT_TRTM_CLS_CODE"]:
                fields[menu] = recvvalue[i]
            else:
                fields[menu] = float(recvvalue[i])
            i += 1
    
    return fields