    if msg_store.count() == msg_quorum:
        # compare 1 and 2, if equal send C2Agent message
        for i in range(1, msg_quorum, 1):
            try:
                msg1 = msg_store.read_one(i)
                log.debug("msg1: " + msg1)
                msg2 = msg_store.read_one(i+1)
                log.debug("msg2: " + msg2)
               
                # date_formats = [
                #     "%m/%d/%Y %H:%M:%S",
                #     "%Y/%m/%d %H:%M:%S",
                #     "%m/%d/%Y %H:%M",
                #     "%Y/%m/%d %H:%M",
                #     "%m/%d/%Y %H"
                # ]
                
                #-------------------------------------------
                data1 = json.loads(msg1)
                msg1_start_date_time = data1["start_date_time"]
                #dt1 = datetime.strptime(msg1_start_date_time, date_format)
                # for fmt in date_formats:
                #     try:
                #         dt1 = datetime.strptime(msg1_start_date_time, fmt)
                #         log.debug(f"Parsed successfully: {dt1} (format: {fmt})")
                #         break
                #     except ValueError:
                #         continue
                # else:
                #     log.debug("No matching format found." + msg1_start_date_time)
               
                convertDateTime = ConvertDateTime()
                dt1 = convertDateTime.convert(msg1_start_date_time)
                # if dt1x == dt1:
                #     log.debug("SAME SAME")

                msg1_peak_lmp = data1["peak_lmp"]
                flmp1 = float(msg1_peak_lmp)
                ilmp1 = int(flmp1)
                msg1_award_level = data1["award_level"]

                #-------------------------------------------
                data2 = json.loads(msg2)
                msg2_start_date_time = data2["start_date_time"]
                #dt2 = datetime.strptime(msg2_start_date_time, date_format)

                # for fmt in date_formats:
                #     try:
                #         dt2 = datetime.strptime(msg2_start_date_time, fmt)
                #         log.debug(f"Parsed successfully: {dt2} (format: {fmt})")
                #         break
                #     except ValueError:
                #         continue
                # else:
                #     log.debug("No matching format found." + msg2_start_date_time)

                dt2 = convertDateTime.convert(msg2_start_date_time)

                msg2_peak_lmp = data2["peak_lmp"]
                flmp2 = float(msg2_peak_lmp)
                ilmp2 = int(flmp2)
                msg2_award_level = data2["award_level"]

                failed_test = False
            
                log.debug("STARTING TEST")
            
                if dt1 == dt2:
                    if ilmp1 == ilmp2:
                        if msg1_award_level == msg2_award_level:
                            log.debug("BINGO: " + msg1)
                            print("BINGO: " + msg1)
                            clientMQ.publish(MQTT_TOPIC_C2AGENT, msg1)
                            log.debug("SENT C2AGENT Msg: " + msg1)
                        else:
                            log.debug("AWARD LEVEL DOES NOT MATCH: " + msg1_award_level + "," + msg2_award_level)
                            failed_test = True
                    else:
                        log.debug("PEAK LMP DOES NOT MATCH: " + msg1_peak_lmp + "," + msg2_peak_lmp)
                        failed_test = True
                else:
                    log.debug("DATETIME DOES NOT MATCH: " + msg1_start_date_time + "." + msg2_start_date_time)
                    failed_test = True
                
                if failed_test == True:
                    log.debug("BOGUS: " + msg1)
                    log.debug("BOGUS: " + msg2)
                    print("BOGUS: " + msg1)
                    print("BOGUS: " + msg2)
                    print("all records: ", msg_store.read_all())
                else:
                    pass
                log.debug("ENDING TEST")

            except Exception as e:
                print(f"An error occurred: {e}")
                log.error(f"An error occurred: {e}")
    else:
        pass
