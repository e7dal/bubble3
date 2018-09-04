Feature: util_cather_catch
Scenario: util_cather_catch
    Given a file named "run_script.py" with:
        """
        import bubble3
        import bubble3.util.catcher as cc
        
        gbc=bubble3.Bubble()
        gbc.set_verbose(0)
        try:
            zerodiv=1/0
        except:
            cc.catch(gbc=gbc)
        
        def err():
            try:
                zerodiv=1/0
            except:
                cc.catch(gbc=gbc)
                
        err()
        
        
        def ign():
            try:
                zerodiv=1/0
            except:
                cc.catch(ignore=[ZeroDivisionError],was_doing='nothing',helpfull_tips='just never do it again',gbc=gbc)
                
        ign()
        

        """
    Given a file named "run_and_save_output.sh" with:
        """
        python run_script.py > run_result.txt 2>&1
        """        
    When I run "sh run_and_save_output.sh"
    When I run "cp ../test_data/expected_outputs/tl_catcher_catch_expected_output.txt expected_output.txt"
    When I run "sed -i 's/datetime.timedelta(0, 0, ....)/NOTIME/g' expected_output.txt"
    When I run "sed -i 's/datetime.timedelta(0, 0, ....)/NOTIME/g' run_result.txt"
    When I run "diff --report-identical-files expected_output.txt run_result.txt"
    Then the command output should contain "Files expected_output.txt and run_result.txt are identical"
    And the command returncode is "0"

