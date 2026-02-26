# Tushare Database整理

## 基本面数据


### 1. db_name='raw_tushare', table_name='balance'

仅保留实际存在的列；增加「数据类型」「非空数量」列。

| 列名                       | 描述                                             | 数据类型    | 非空数量 |
| -------------------------- | ------------------------------------------------ | ----------- | -------- |
| InnerCode                  | 内部代码 / 股票代码                                     | object     | 246752  |
| ann_date                   | 公告日期                                            | datetime64 | 246752  |
| f_ann_date                 | 实际公告日期                                          | datetime64 | 246752  |
| end_date                   | 报告期                                             | datetime64 | 246752  |
| report_type                | 报告类型                                            | object     | 246752  |
| comp_type                  | 公司类型 (1 一般工商业 2 银行 3 保险 4 证券)                   | object     | 246752  |
| end_type                   | 报告期类型                                           | object     | 246319  |
| total_share                | 期末总股本                                           | float64    | 246042  |
| cap_rese                   | 资本公积金                                           | float64    | 244871  |
| undistr_porfit             | 未分配利润                                           | float64    | 246025  |
| surplus_rese               | 盈余公积金                                           | float64    | 242644  |
| special_rese               | 专项储备                                            | float64    | 62806   |
| money_cap                  | 货币资金                                            | float64    | 243509  |
| trad_asset                 | 交易性金融资产                                         | float64    | 107831  |
| notes_receiv               | 应收票据                                            | float64    | 176377  |
| accounts_receiv            | 应收账款                                            | float64    | 239066  |
| oth_receiv                 | 其他应收款                                           | float64    | 154624  |
| prepayment                 | 预付款项                                            | float64    | 239792  |
| div_receiv                 | 应收股利                                            | float64    | 30407   |
| int_receiv                 | 应收利息                                            | float64    | 51139   |
| inventories                | 存货                                              | float64    | 236884  |
| amor_exp                   | 待摊费用                                            | float64    | 2       |
| nca_within_1y              | 一年内到期的非流动资产                                     | float64    | 43543   |
| sett_rsrv                  | 结算备付金                                           | float64    | 5696    |
| loanto_oth_bank_fi         | 拆出资金                                            | float64    | 5507    |
| premium_receiv             | 应收保费                                            | float64    | 3176    |
| reinsur_receiv             | 应收分保账款                                          | float64    | 3126    |
| reinsur_res_receiv         | 应收分保合同准备金                                       | float64    | 2834    |
| pur_resale_fa              | 买入返售金融资产                                        | float64    | 8538    |
| oth_cur_assets             | 其他流动资产                                          | float64    | 232365  |
| total_cur_assets           | 流动资产合计                                          | float64    | 241300  |
| fa_avail_for_sale          | 可供出售金融资产                                        | float64    | 52284   |
| htm_invest                 | 持有至到期投资                                         | float64    | 3788    |
| lt_eqt_invest              | 长期股权投资                                          | float64    | 157114  |
| invest_real_estate         | 投资性房地产                                          | float64    | 113722  |
| time_deposits              | 定期存款                                            | float64    | 297     |
| oth_assets                 | 其他资产                                            | float64    | 4898    |
| lt_rec                     | 长期应收款                                           | float64    | 49560   |
| fix_assets                 | 固定资产                                            | float64    | 220715  |
| cip                        | 在建工程                                            | float64    | 181271  |
| const_materials            | 工程物资                                            | float64    | 28988   |
| fixed_assets_disp          | 固定资产清理                                          | float64    | 24159   |
| produc_bio_assets          | 生产性生物资产                                         | float64    | 11108   |
| oil_and_gas_assets         | 油气资产                                            | float64    | 4249    |
| intan_assets               | 无形资产                                            | float64    | 243123  |
| r_and_d                    | 研发支出                                            | float64    | 49058   |
| goodwill                   | 商誉                                              | float64    | 121390  |
| lt_amor_exp                | 长期待摊费用                                          | float64    | 206558  |
| defer_tax_assets           | 递延所得税资产                                         | float64    | 237597  |
| decr_in_disbur             | 发放贷款及垫款                                         | float64    | 8984    |
| oth_nca                    | 其他非流动资产                                         | float64    | 191473  |
| total_nca                  | 非流动资产合计                                         | float64    | 241184  |
| cash_reser_cb              | 现金及存放中央银行款项                                     | float64    | 2710    |
| depos_in_oth_bfi           | 存放同业和其它金融机构款项                                   | float64    | 2329    |
| prec_metals                | 贵金属                                             | float64    | 1001    |
| deriv_assets               | 衍生金融资产                                          | float64    | 15213   |
| rr_reins_une_prem          | 应收分保未到期责任准备金                                    | float64    | 184     |
| rr_reins_outstd_cla        | 应收分保未决赔款准备金                                     | float64    | 184     |
| rr_reins_lins_liab         | 应收分保寿险责任准备金                                     | float64    | 162     |
| rr_reins_lthins_liab       | 应收分保长期健康险责任准备金                                  | float64    | 163     |
| refund_depos               | 存出保证金                                           | float64    | 2107    |
| ph_pledge_loans            | 保户质押贷款                                          | float64    | 155     |
| refund_cap_depos           | 存出资本保证金                                         | float64    | 301     |
| indep_acct_assets          | 独立账户资产                                          | float64    | 138     |
| client_depos               | 其中：客户资金存款                                       | float64    | 2087    |
| client_prov                | 其中：客户备付金                                        | float64    | 2091    |
| transac_seat_fee           | 其中：交易席位费                                        | float64    | 26      |
| invest_as_receiv           | 应收款项类投资                                         | float64    | 645     |
| total_assets               | 资产总计                                            | float64    | 246733  |
| lt_borr                    | 长期借款                                            | float64    | 130210  |
| st_borr                    | 短期借款                                            | float64    | 186550  |
| cb_borr                    | 向中央银行借款                                         | float64    | 5085    |
| depos_ib_deposits          | 吸收存款及同业存放                                       | float64    | 4191    |
| loan_oth_bank              | 拆入资金                                            | float64    | 7710    |
| trading_fl                 | 交易性金融负债                                         | float64    | 24145   |
| notes_payable              | 应付票据                                            | float64    | 150570  |
| acct_payable               | 应付账款                                            | float64    | 227117  |
| adv_receipts               | 预收款项                                            | float64    | 145427  |
| sold_for_repur_fa          | 卖出回购金融资产款                                       | float64    | 8425    |
| comm_payable               | 应付手续费及佣金                                        | float64    | 3245    |
| payroll_payable            | 应付职工薪酬                                          | float64    | 244934  |
| taxes_payable              | 应交税费                                            | float64    | 245927  |
| int_payable                | 应付利息                                            | float64    | 95799   |
| div_payable                | 应付股利                                            | float64    | 78972   |
| oth_payable                | 其他应付款                                           | float64    | 160873  |
| acc_exp                    | 预提费用                                            | float64    | 13      |
| deferred_inc               | 递延收益                                            | float64    | 105     |
| st_bonds_payable           | 应付短期债券                                          | float64    | 484     |
| payable_to_reinsurer       | 应付分保账款                                          | float64    | 3044    |
| rsrv_insur_cont            | 保险合同准备金                                         | float64    | 2661    |
| acting_trading_sec         | 代理买卖证券款                                         | float64    | 5309    |
| acting_uw_sec              | 代理承销证券款                                         | float64    | 3234    |
| non_cur_liab_due_1y        | 一年内到期的非流动负债                                     | float64    | 164863  |
| oth_cur_liab               | 其他流动负债                                          | float64    | 152624  |
| total_cur_liab             | 流动负债合计                                          | float64    | 241320  |
| bond_payable               | 应付债券                                            | float64    | 44500   |
| lt_payable                 | 长期应付款                                           | float64    | 44864   |
| specific_payables          | 专项应付款                                           | float64    | 29799   |
| estimated_liab             | 预计负债                                            | float64    | 82626   |
| defer_tax_liab             | 递延所得税负债                                         | float64    | 165672  |
| defer_inc_non_cur_liab     | 递延收益 - 非流动负债                                    | float64    | 200191  |
| oth_ncl                    | 其他非流动负债                                         | float64    | 35977   |
| total_ncl                  | 非流动负债合计                                         | float64    | 235193  |
| depos_oth_bfi              | 同业和其它金融机构存放款项                                   | float64    | 2272    |
| deriv_liab                 | 衍生金融负债                                          | float64    | 14837   |
| depos                      | 吸收存款                                            | float64    | 2347    |
| agency_bus_liab            | 代理业务负债                                          | Int32      | 0       |
| oth_liab                   | 其他负债                                            | float64    | 4850    |
| prem_receiv_adva           | 预收保费                                            | float64    | 304     |
| depos_received             | 存入保证金                                           | Int32      | 0       |
| ph_invest                  | 保户储金及投资款                                        | float64    | 223     |
| reser_une_prem             | 未到期责任准备金                                        | float64    | 188     |
| reser_outstd_claims        | 未决赔款准备金                                         | float64    | 188     |
| reser_lins_liab            | 寿险责任准备金                                         | float64    | 167     |
| reser_lthins_liab          | 长期健康险责任准备金                                      | float64    | 167     |
| indept_acc_liab            | 独立账户负债                                          | float64    | 139     |
| pledge_borr                | 其中：质押借款                                         | Int32      | 0       |
| indem_payable              | 应付赔付款                                           | float64    | 229     |
| policy_div_payable         | 应付保户红利                                          | float64    | 181     |
| total_liab                 | 负债合计                                            | float64    | 246617  |
| treasury_share             | 减：库存股                                           | float64    | 66311   |
| ordin_risk_reser           | 一般风险准备                                          | float64    | 12653   |
| forex_differ               | 外币报表折算差额                                        | float64    | 64      |
| invest_loss_unconf         | 未确认的投资损失                                        | float64    | 3       |
| minority_int               | 少数股东权益                                          | float64    | 188835  |
| total_hldr_eqy_exc_min_int | 股东权益合计 (不含少数股东权益)                               | float64    | 246690  |
| total_hldr_eqy_inc_min_int | 股东权益合计 (含少数股东权益)                                | float64    | 246481  |
| total_liab_hldr_eqy        | 负债及股东权益总计                                       | float64    | 246591  |
| lt_payroll_payable         | 长期应付职工薪酬                                        | float64    | 29663   |
| oth_comp_income            | 其他综合收益                                          | float64    | 152622  |
| oth_eqt_tools              | 其他权益工具                                          | float64    | 22274   |
| oth_eqt_tools_p_shr        | 其他权益工具 (优先股)                                    | float64    | 4374    |
| lending_funds              | 融出资金                                            | float64    | 2117    |
| acc_receivable             | 应收款项                                            | float64    | 2174    |
| st_fin_payable             | 应付短期融资款                                         | float64    | 2001    |
| payables                   | 应付款项                                            | float64    | 2132    |
| hfs_assets                 | 持有待售的资产                                         | float64    | 11640   |
| hfs_sales                  | 持有待售的负债                                         | float64    | 4564    |
| cost_fin_assets            | 以摊余成本计量的金融资产                                    | float64    | 501     |
| fair_value_fin_assets      | 以公允价值计量且其变动计入其他综合收益的金融资产                        | float64    | 500     |
| contract_assets            | 合同资产                                            | float64    | 48854   |
| contract_liab              | 合同负债                                            | float64    | 135336  |
| accounts_receiv_bill       | 应收票据及应收账款                                       | float64    | 238298  |
| accounts_pay               | 应付票据及应付账款                                       | float64    | 238982  |
| oth_rcv_total              | 其他应收款 (合计)(元)                                   | float64    | 239379  |
| fix_assets_total           | 固定资产 (合计)(元)                                    | float64    | 239430  |
| cip_total                  | 在建工程 (合计)(元)                                    | float64    | 205542  |
| oth_pay_total              | 其他应付款 (合计)(元)                                   | float64    | 239341  |
| long_pay_total             | 长期应付款 (合计)(元)                                   | float64    | 84204   |
| debt_invest                | 债权投资 (元)                                        | float64    | 11839   |
| oth_debt_invest            | 其他债权投资 (元)                                      | float64    | 7404    |
| update_flag                | 更新标识                                            | object     | 246752  |

------

### 2. db_name='raw_tushare', table_name='cashflow'

仅保留实际存在的列；增加「数据类型」「非空数量」列。

| 列名                         | 描述                                               | 数据类型    | 非空数量 |
| ---------------------------- | -------------------------------------------------- | ----------- | -------- |
| InnerCode                    | 内部代码 / 股票代码                                | object      | 230594   |
| ann_date                     | 公告日期                                           | datetime64  | 230594   |
| f_ann_date                   | 实际公告日期                                       | datetime64  | 230594   |
| end_date                     | 报告期                                             | datetime64  | 230594   |
| comp_type                    | 公司类型 (1 一般工商业 2 银行 3 保险 4 证券)       | object      | 230594   |
| report_type                  | 报表类型                                           | object      | 230594   |
| end_type                     | 报告期类型                                         | object      | 230571   |
| net_profit                   | 净利润                                             | float64     | 120037   |
| finan_exp                    | 财务费用                                           | float64     | 113035   |
| c_fr_sale_sg                 | 销售商品、提供劳务收到的现金                       | float64     | 225684   |
| recp_tax_rends               | 收到的税费返还                                     | float64     | 170265   |
| n_depos_incr_fi              | 客户存款和同业存放款项净增加额                     | float64     | 5518     |
| n_incr_loans_cb              | 向中央银行借款净增加额                             | float64     | 3817     |
| n_inc_borr_oth_fi            | 向其他金融机构拆入资金净增加额                     | float64     | 2868     |
| prem_fr_orig_contr           | 收到原保险合同保费取得的现金                       | float64     | 2816     |
| n_incr_insured_dep           | 保户储金净增加额                                   | float64     | 2609     |
| n_reinsur_prem               | 收到再保业务现金净额                               | float64     | 2481     |
| n_incr_disp_tfa              | 处置交易性金融资产净增加额                         | float64     | 1126     |
| ifc_cash_incr                | 收取利息和手续费净增加额                           | float64     | 11761    |
| n_incr_disp_faas             | 处置可供出售金融资产净增加额                       | float64     | 32       |
| n_incr_loans_oth_bank        | 拆入资金净增加额                                   | float64     | 5119     |
| n_cap_incr_repur             | 回购业务资金净增加额                               | float64     | 4593     |
| c_fr_oth_operate_a           | 收到其他与经营活动有关的现金                       | float64     | 230246   |
| c_inf_fr_operate_a           | 经营活动现金流入小计                               | float64     | 230416   |
| c_paid_goods_s               | 购买商品、接受劳务支付的现金                       | float64     | 225457   |
| c_paid_to_for_empl           | 支付给职工以及为职工支付的现金                     | float64     | 230340   |
| c_paid_for_taxes             | 支付的各项税费                                     | float64     | 230216   |
| n_incr_clt_loan_adv          | 客户贷款及垫款净增加额                             | float64     | 8605     |
| n_incr_dep_cbob              | 存放央行和同业款项净增加额                         | float64     | 4643     |
| c_pay_claims_orig_inco       | 支付原保险合同赔付款项的现金                       | float64     | 2756     |
| pay_handling_chrg            | 支付手续费的现金                                   | float64     | 9848     |
| pay_comm_insur_plcy          | 支付保单红利的现金                                 | float64     | 2672     |
| oth_cash_pay_oper_act        | 支付其他与经营活动有关的现金                       | float64     | 230376   |
| st_cash_out_act              | 经营活动现金流出小计                               | float64     | 230407   |
| n_cashflow_act               | 经营活动产生的现金流量净额                         | float64     | 230552   |
| oth_recp_ral_inv_act         | 收到其他与投资活动有关的现金                       | float64     | 92538    |
| c_disp_withdrwl_invest       | 收回投资收到的现金                                 | float64     | 132484   |
| c_recp_return_invest         | 取得投资收益收到的现金                             | float64     | 156087   |
| n_recp_disp_fiolta           | 处置固定资产、无形资产和其他长期资产收回的现金净额 | float64     | 176136   |
| n_recp_disp_sobu             | 处置子公司及其他营业单位收到的现金净额             | float64     | 29668    |
| stot_inflows_inv_act         | 投资活动现金流入小计                               | float64     | 214615   |
| c_pay_acq_const_fiolta       | 购建固定资产、无形资产和其他长期资产支付的现金     | float64     | 228528   |
| c_paid_invest                | 投资支付的现金                                     | float64     | 149880   |
| n_disp_subs_oth_biz          | 取得子公司及其他营业单位支付的现金净额             | float64     | 33720    |
| oth_pay_ral_inv_act          | 支付其他与投资活动有关的现金                       | float64     | 85110    |
| n_incr_pledge_loan           | 质押贷款净增加额                                   | float64     | 2915     |
| stot_out_inv_act             | 投资活动现金流出小计                               | float64     | 229170   |
| n_cashflow_inv_act           | 投资活动产生的现金流量净额                         | float64     | 229691   |
| c_recp_borrow                | 取得借款收到的现金                                 | float64     | 172765   |
| proc_issue_bonds             | 发行债券收到的现金                                 | float64     | 10207    |
| oth_cash_recp_ral_fnc_act    | 收到其他与筹资活动有关的现金                       | float64     | 93482    |
| stot_cash_in_fnc_act         | 筹资活动现金流入小计                               | float64     | 198047   |
| free_cashflow                | 企业自由现金流量                                   | float64     | 198609   |
| c_prepay_amt_borr            | 偿还债务支付的现金                                 | float64     | 180412   |
| c_pay_dist_dpcp_int_exp      | 分配股利、利润或偿付利息支付的现金                 | float64     | 212596   |
| incl_dvd_profit_paid_sc_ms   | 其中：子公司支付给少数股东的股利、利润             | float64     | 42742    |
| oth_cashpay_ral_fnc_act      | 支付其他与筹资活动有关的现金                       | float64     | 168972   |
| stot_cashout_fnc_act         | 筹资活动现金流出小计                               | float64     | 222159   |
| n_cash_flows_fnc_act         | 筹资活动产生的现金流量净额                         | float64     | 224114   |
| eff_fx_flu_cash              | 汇率变动对现金的影响                               | float64     | 171551   |
| n_incr_cash_cash_equ         | 现金及现金等价物净增加额                           | float64     | 230533   |
| c_cash_equ_beg_period        | 期初现金及现金等价物余额                           | float64     | 230377   |
| c_cash_equ_end_period        | 期末现金及现金等价物余额                           | float64     | 230419   |
| c_recp_cap_contrib           | 吸收投资收到的现金                                 | float64     | 90469    |
| incl_cash_rec_saims          | 其中：子公司吸收少数股东投资收到的现金             | float64     | 48037    |
| uncon_invest_loss            | 未确认投资损失                                     | Int32       | 0        |
| prov_depr_assets             | 加：资产减值准备                                   | float64     | 110889   |
| depr_fa_coga_dpba            | 固定资产折旧、油气资产折耗、生产性生物资产折旧     | float64     | 119402   |
| amort_intang_assets          | 无形资产摊销                                       | float64     | 117903   |
| lt_amor_deferred_exp         | 长期待摊费用摊销                                   | float64     | 102006   |
| decr_deferred_exp            | 待摊费用减少                                       | float64     | 62       |
| incr_acc_exp                 | 预提费用增加                                       | float64     | 19       |
| loss_disp_fiolta             | 处置固定资产、无形资产和其他长期资产的损失         | float64     | 97074    |
| loss_scr_fa                  | 固定资产报废损失                                   | float64     | 68999    |
| loss_fv_chg                  | 公允价值变动损失                                   | float64     | 54682    |
| invest_loss                  | 投资损失                                           | float64     | 104830   |
| decr_def_inc_tax_assets      | 递延所得税资产减少                                 | float64     | 113292   |
| incr_def_inc_tax_liab        | 递延所得税负债增加                                 | float64     | 75926    |
| decr_inventories             | 存货的减少                                         | float64     | 115681   |
| decr_oper_payable            | 经营性应收项目的减少                               | float64     | 119938   |
| incr_oper_payable            | 经营性应付项目的增加                               | float64     | 119947   |
| others                       | 其他                                               | float64     | 8685     |
| im_net_cashflow_oper_act     | 经营活动产生的现金流量净额 (间接法)                | float64     | 120035   |
| conv_debt_into_cap           | 债务转为资本                                       | float64     | 789      |
| conv_copbonds_due_within_1y  | 一年内到期的可转换公司债券                         | float64     | 480      |
| fa_fnc_leases                | 融资租入固定资产                                   | float64     | 1073     |
| im_n_incr_cash_equ           | 现金及现金等价物净增加额 (间接法)                  | float64     | 118390   |
| net_dism_capital_add         | 拆出资金净增加额                                   | float64     | 2046     |
| net_cash_rece_sec            | 代理买卖证券收到的现金净额 (元)                    | float64     | 3062     |
| credit_impa_loss             | 信用减值损失                                       | float64     | 39280    |
| use_right_asset_dep          | 使用权资产折旧                                     | float64     | 45682    |
| oth_loss_asset               | 其他资产减值损失                                   | float64     | 24       |
| end_bal_cash                 | 现金的期末余额                                     | float64     | 118360   |
| beg_bal_cash                 | 减：现金的期初余额                                 | float64     | 118339   |
| end_bal_cash_equ             | 加：现金等价物的期末余额                           | float64     | 4070     |
| beg_bal_cash_equ             | 减：现金等价物的期初余额                           | float64     | 4152     |
| update_flag                  | 更新标识                                           | object      | 230594   |

------

### 3. db_name='raw_tushare', table_name='fina_indicator'

仅保留实际存在的列；增加「数据类型」「非空数量」列。

| 列名                         | 描述                                                         | 数据类型    | 非空数量 |
| ---------------------------- | ------------------------------------------------------------ | ----------- | -------- |
| InnerCode                  | 内部代码 / 股票代码                                             | object     | 393298  |
| ann_date                   | 公告日期                                                    | datetime64 | 393277  |
| end_date                   | 报告期                                                     | datetime64 | 393298  |
| eps                        | 基本每股收益                                                  | float64    | 374911  |
| dt_eps                     | 稀释每股收益                                                  | float64    | 364916  |
| total_revenue_ps           | 每股营业总收入                                                 | float64    | 376347  |
| revenue_ps                 | 每股营业收入                                                  | float64    | 376304  |
| capital_rese_ps            | 每股资本公积                                                  | float64    | 374641  |
| surplus_rese_ps            | 每股盈余公积                                                  | float64    | 370665  |
| undist_profit_ps           | 每股未分配利润                                                 | float64    | 376869  |
| extra_item                 | 非经常性损益                                                  | float64    | 377781  |
| profit_dedt                | 扣除非经常性损益后的净利润 (扣非净利润)                                   | float64    | 377770  |
| gross_margin               | 毛利                                                      | float64    | 384314  |
| current_ratio              | 流动比率                                                    | float64    | 371806  |
| quick_ratio                | 速动比率                                                    | float64    | 371448  |
| cash_ratio                 | 保守速动比率                                                  | float64    | 369830  |
| ar_turn                    | 应收账款周转率                                                 | float64    | 368973  |
| ca_turn                    | 流动资产周转率                                                 | float64    | 372125  |
| fa_turn                    | 固定资产周转率                                                 | float64    | 384534  |
| assets_turn                | 总资产周转率                                                  | float64    | 380226  |
| op_income                  | 经营活动净收益                                                 | float64    | 392632  |
| ebit                       | 息税前利润                                                   | float64    | 384962  |
| ebitda                     | 息税折旧摊销前利润                                               | float64    | 205087  |
| fcff                       | 企业自由现金流量                                                | float64    | 364760  |
| fcfe                       | 股权自由现金流量                                                | float64    | 363314  |
| current_exint              | 无息流动负债                                                  | float64    | 369854  |
| noncurrent_exint           | 无息非流动负债                                                 | float64    | 357081  |
| interestdebt               | 带息债务                                                    | float64    | 370835  |
| netdebt                    | 净债务                                                     | float64    | 370835  |
| tangible_asset             | 有形资产                                                    | float64    | 371044  |
| working_capital            | 营运资金                                                    | float64    | 370139  |
| networking_capital         | 营运流动资本                                                  | float64    | 369854  |
| invest_capital             | 全部投入资本                                                  | float64    | 371150  |
| retained_earnings          | 留存收益                                                    | float64    | 376895  |
| diluted2_eps               | 期末摊薄每股收益                                                | float64    | 376893  |
| bps                        | 每股净资产                                                   | float64    | 376899  |
| ocfps                      | 每股经营活动产生的现金流量净额                                         | float64    | 377666  |
| retainedps                 | 每股留存收益                                                  | float64    | 376883  |
| cfps                       | 每股现金流量净额                                                | float64    | 376752  |
| ebit_ps                    | 每股息税前利润                                                 | float64    | 369830  |
| fcff_ps                    | 每股企业自由现金流量                                              | float64    | 359705  |
| fcfe_ps                    | 每股股东自由现金流量                                              | float64    | 359705  |
| netprofit_margin           | 销售净利率                                                   | float64    | 391374  |
| grossprofit_margin         | 销售毛利率                                                   | float64    | 383442  |
| cogs_of_sales              | 销售成本率                                                   | float64    | 383442  |
| expense_of_sales           | 销售期间费用率                                                 | float64    | 383714  |
| profit_to_gr               | 净利润 / 营业总收入                                             | float64    | 391417  |
| saleexp_to_gr              | 销售费用 / 营业总收入                                            | float64    | 376704  |
| adminexp_of_gr             | 管理费用 / 营业总收入                                            | float64    | 390946  |
| finaexp_of_gr              | 财务费用 / 营业总收入                                            | float64    | 383651  |
| impai_ttm                  | 资产减值损失 / 营业总收入                                          | float64    | 319107  |
| gc_of_gr                   | 营业总成本 / 营业总收入                                           | float64    | 383809  |
| op_of_gr                   | 营业利润 / 营业总收入                                            | float64    | 391378  |
| ebit_of_gr                 | 息税前利润 / 营业总收入                                           | float64    | 384142  |
| roe                        | 净资产收益率                                                  | float64    | 388172  |
| roe_waa                    | 加权平均净资产收益率                                              | float64    | 370366  |
| roe_dt                     | 净资产收益率 (扣除非经常损益)                                        | float64    | 373649  |
| roa                        | 总资产报酬率                                                  | float64    | 384934  |
| npta                       | 总资产净利润                                                  | float64    | 392220  |
| roic                       | 投入资本回报率                                                 | float64    | 382690  |
| roe_yearly                 | 年化净资产收益率                                                | float64    | 388171  |
| roa2_yearly                | 年化总资产报酬率                                                | float64    | 384933  |
| debt_to_assets             | 资产负债率                                                   | float64    | 377913  |
| assets_to_eqt              | 权益乘数                                                    | float64    | 373615  |
| dp_assets_to_eqt           | 权益乘数 (杜邦分析)                                             | float64    | 371038  |
| ca_to_assets               | 流动资产 / 总资产                                              | float64    | 370116  |
| nca_to_assets              | 非流动资产 / 总资产                                             | float64    | 369991  |
| tbassets_to_totalassets    | 有形资产 / 总资产                                              | float64    | 371023  |
| int_to_talcap              | 带息债务 / 全部投入资本                                           | float64    | 368397  |
| eqt_to_talcapital          | 归属于母公司的股东权益 / 全部投入资本                                    | float64    | 368357  |
| currentdebt_to_debt        | 流动负债 / 负债合计                                             | float64    | 370127  |
| longdeb_to_debt            | 非流动负债 / 负债合计                                            | float64    | 356949  |
| ocf_to_shortdebt           | 经营活动产生的现金流量净额 / 流动负债                                    | float64    | 370003  |
| debt_to_eqt                | 负债合计 / 归属于母公司的股东权益                                      | float64    | 373227  |
| eqt_to_debt                | 归属于母公司的股东权益 / 负债合计                                      | float64    | 377823  |
| eqt_to_interestdebt        | 归属于母公司的股东权益 / 带息债务                                      | float64    | 327851  |
| tangibleasset_to_debt      | 有形资产 / 负债合计                                             | float64    | 370724  |
| tangasset_to_intdebt       | 有形资产 / 带息债务                                             | float64    | 327851  |
| tangibleasset_to_netdebt   | 有形资产 / 净债务                                              | float64    | 173233  |
| ocf_to_debt                | 经营活动产生的现金流量净额 / 负债合计                                    | float64    | 377590  |
| turn_days                  | 营业周期                                                    | float64    | 371234  |
| roa_yearly                 | 年化总资产报酬率                                                | float64    | 392219  |
| roa_dp                     | 总资产报酬率 (杜邦)                                             | float64    | 375437  |
| fixed_assets               | 固定资产合计                                                  | float64    | 376710  |
| profit_to_op               | 营业利润 / 营业收入                                             | float64    | 391388  |
| q_saleexp_to_gr            | 销售费用 / 营业总收入 (单季度)                                      | float64    | 343135  |
| q_gc_to_gr                 | 营业总成本 / 营业总收入 (单季度)                                     | float64    | 349473  |
| q_roe                      | 净资产收益率 (单季度)                                            | float64    | 352421  |
| q_dt_roe                   | 净资产收益率 (单季度)(扣除非经常损益)                                   | float64    | 332254  |
| q_npta                     | 总资产净利润 (单季度)                                            | float64    | 356134  |
| q_ocf_to_sales             | 经营活动产生的现金流量净额 / 营业收入 (单季度)                              | float64    | 355978  |
| basic_eps_yoy              | 基本每股收益同比增长率 (%)                                         | float64    | 363932  |
| dt_eps_yoy                 | 稀释每股收益同比增长率 (%)                                         | float64    | 353506  |
| cfps_yoy                   | 每股经营活动产生的现金流量净额同比增长率 (%)                                | float64    | 352081  |
| op_yoy                     | 营业利润同比增长率 (%)                                           | float64    | 369542  |
| ebt_yoy                    | 利润总额同比增长率 (%)                                           | float64    | 369710  |
| netprofit_yoy              | 归属母公司股东的净利润同比增长率 (%)                                    | float64    | 370447  |
| dt_netprofit_yoy           | 扣除非经常损益净利润同比增长率 (%)                                     | float64    | 363721  |
| ocf_yoy                    | 经营活动产生的现金流量净额同比增长率 (%)                                  | float64    | 369315  |
| roe_yoy                    | 净资产收益率同比增长率 (%)                                         | float64    | 346925  |
| bps_yoy                    | 每股净资产同比增长率 (%)                                          | float64    | 374004  |
| assets_yoy                 | 总资产同比增长率 (%)                                            | float64    | 375964  |
| eqt_yoy                    | 归属于母公司股东权益同比增长率 (%)                                     | float64    | 375783  |
| tr_yoy                     | 营业收入同比增长率 (%)                                           | float64    | 369576  |
| or_yoy                     | 营业总收入同比增长率 (%)                                          | float64    | 369509  |
| q_sales_yoy                | 营业收入同比增长率 (%)(单季度)                                      | float64    | 330335  |
| q_op_qoq                   | 营业利润环比增长率 (%)(单季度)                                      | float64    | 351917  |
| equity_yoy                 | 股东权益同比增长率 (%)                                           | float64    | 352552  |
| update_flag                | 更新标识                                                    | object     | 393298  |

------

### 4. db_name='raw_tushare', table_name='income'


| 列名                      | 描述                                         | 数据类型     | 非空数量 |
| ------------------------- | -------------------------------------------- | ----------- | -------- |
| InnerCode                 | 内部代码 / 股票代码                          | object      | 267717   |
| ann_date                  | 公告日期                                     | datetime64  | 267717   |
| f_ann_date                | 实际公告日期                                 | datetime64  | 267717   |
| end_date                  | 报告期                                       | datetime64  | 267717   |
| report_type               | 报告类型                                     | object      | 267717   |
| comp_type                 | 公司类型 (1 一般工商业 2 银行 3 保险 4 证券) | object      | 267717   |
| end_type                  | 报告期类型                                   | object      | 267414   |
| basic_eps                 | 基本每股收益                                 | float64     | 265630   |
| diluted_eps               | 稀释每股收益                                 | float64     | 259082   |
| total_revenue             | 营业总收入                                   | float64     | 267352   |
| revenue                   | 营业收入                                     | float64     | 267322   |
| int_income                | 利息收入                                     | float64     | 12202    |
| prem_earned               | 已赚保费                                     | float64     | 3454     |
| comm_income               | 手续费及佣金收入                             | float64     | 7717     |
| n_commis_income           | 手续费及佣金净收入                           | float64     | 4944     |
| n_oth_income              | 其他经营净收益                               | float64     | 5128     |
| n_oth_b_income            | 加：其他业务净收益                           | float64     | 5112     |
| prem_income               | 保险业务收入                                 | float64     | 277      |
| out_prem                  | 减：分出保费                                 | float64     | 261      |
| une_prem_reser            | 提取未到期责任准备金                         | float64     | 261      |
| reins_income              | 其中：分保费收入                             | float64     | 183      |
| n_sec_tb_income           | 代理买卖证券业务净收入                       | float64     | 2339     |
| n_sec_uw_income           | 证券承销业务净收入                           | float64     | 2307     |
| n_asset_mg_income         | 受托客户资产管理业务净收入                   | float64     | 2339     |
| oth_b_income              | 其他业务收入                                 | float64     | 5212     |
| fv_value_chg_gain         | 加：公允价值变动净收益                       | float64     | 118779   |
| invest_income             | 加：投资净收益                               | float64     | 234414   |
| ass_invest_income         | 其中：对联营企业和合营企业的投资收益         | float64     | 140836   |
| forex_gain                | 加：汇兑净收益                               | float64     | 10037    |
| total_cogs                | 营业总成本                                   | float64     | 267099   |
| oper_cost                 | 减：营业成本                                 | float64     | 261299   |
| int_exp                   | 减：利息支出                                 | float64     | 9904     |
| comm_exp                  | 减：手续费及佣金支出                         | float64     | 8023     |
| biz_tax_surchg            | 减：营业税金及附加                           | float64     | 266397   |
| sell_exp                  | 减：销售费用                                 | float64     | 256800   |
| admin_exp                 | 减：管理费用                                 | float64     | 267037   |
| fin_exp                   | 减：财务费用                                 | float64     | 261782   |
| assets_impair_loss        | 减：资产减值损失                             | float64     | 214881   |
| prem_refund               | 退保金                                       | float64     | 2462     |
| compens_payout            | 赔付总支出                                   | float64     | 2997     |
| reser_insur_liab          | 提取保险责任准备金                           | float64     | 3353     |
| div_payt                  | 保户红利支出                                 | float64     | 2880     |
| reins_exp                 | 分保费用                                     | float64     | 2003     |
| oper_exp                  | 营业支出                                     | float64     | 5251     |
| compens_payout_refu       | 减：摊回赔付支出                             | float64     | 268      |
| insur_reser_refu          | 减：摊回保险责任准备金                       | float64     | 269      |
| reins_cost_refund         | 减：摊回分保费用                             | float64     | 267      |
| other_bus_cost            | 其他业务成本                                 | float64     | 4461     |
| operate_profit            | 营业利润                                     | float64     | 267257   |
| non_oper_income           | 加：营业外收入                               | float64     | 257966   |
| non_oper_exp              | 减：营业外支出                               | float64     | 258024   |
| nca_disploss              | 其中：减: 非流动资产处置净损失               | float64     | 27427    |
| total_profit              | 利润总额                                     | float64     | 267365   |
| income_tax                | 所得税费用                                   | float64     | 261977   |
| n_income                  | 净利润 (含少数股东损益)                      | float64     | 267342   |
| n_income_attr_p           | 净利润 (不含少数股东损益)                    | float64     | 267705   |
| minority_gain             | 少数股东损益                                 | float64     | 202779   |
| oth_compr_income          | 其他综合收益                                 | float64     | 149882   |
| t_compr_income            | 综合收益总额                                 | float64     | 265708   |
| compr_inc_attr_p          | 归属于母公司 (或股东) 的综合收益总额         | float64     | 265698   |
| compr_inc_attr_m_s        | 归属于少数股东的综合收益总额                 | float64     | 201902   |
| ebit                      | 息税前利润                                   | float64     | 238183   |
| ebitda                    | 息税折旧摊销前利润                           | float64     | 129532   |
| insurance_exp             | 保险业务支出                                 | float64     | 3        |
| undist_profit             | 年初未分配利润                               | float64     | 30       |
| distable_profit           | 可分配利润                                   | float64     | 30       |
| rd_exp                    | 研发费用                                     | float64     | 192289   |
| fin_exp_int_exp           | 财务费用 - 利息费用                          | float64     | 186166   |
| fin_exp_int_inc           | 财务费用 - 利息收入                          | float64     | 202476   |
| transfer_surplus_rese     | 盈余公积转入                                 | Int32       | 0        |
| transfer_housing_imprest  | 住房周转金转入                               | Int32       | 0        |
| transfer_oth              | 其他转入                                     | float64     | 1        |
| adj_lossgain              | 调整以前年度损益                             | float64     | 1        |
| withdra_legal_surplus     | 提取法定盈余公积                             | Int32       | 0        |
| withdra_legal_pubfund     | 提取法定公益金                               | float64     | 1        |
| withdra_biz_devfund       | 提取企业发展基金                             | Int32       | 0        |
| withdra_rese_fund         | 提取储备基金                                 | Int32       | 0        |
| withdra_oth_ersu          | 提取任意盈余公积                             | Int32       | 0        |
| workers_welfare           | 职工奖励及福利                               | Int32       | 0        |
| distr_profit_shrhder      | 可供股东分配的利润                           | float64     | 30       |
| prfshare_payable_dvd      | 应付优先股股利                               | float64     | 1        |
| comshare_payable_dvd      | 应付普通股股利                               | float64     | 12       |
| capit_comstock_div        | 转作股本的普通股股利                         | Int32       | 0        |
| update_flag               | 更新标识                                     | object      | 267717   |
