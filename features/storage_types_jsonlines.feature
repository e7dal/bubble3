Feature: Bubble storage types
Scenario: load mysrclient.py pull and store type jsonlines
  Given a file named ".bubble" with:
            """
            bubble=2016.04.21
            """
    And a file named "./config/config.yaml" with:
            """
            ---
            CFG:
                BUBBLE:
                    STORAGE_TYPE: jsonl
                DEV:
                    SOURCE:    #pull
                        CLIENT: ./mysrcclient.py
            ...
            """
    And a directory named "./remember/archive"
    And a file named "./mysrcclient.py" with:
            """
            from bubble3 import Bubble
            class BubbleClient(Bubble):
                def __init__(self,cfg={}):
                    self.CFG=cfg
                def pull(self, amount=1000, index=0):
                    self.say('BC: %d,%d'%(amount,index))
                    for i in range(amount):
                        it={'keyA':'A_'+str(i),
                                    'keyB':'B_'+str(i),
                                    'keyC':['c',66,{'keyDinList':'D_'+str(i)}]}
                        self.say('BC:yielding:%d %d'%(amount,index),stuff=it,verbosity=100)
                        yield it
            """
    When I run "bubble3 pull"
    Then the command output should contain "pulled [1000] objects"
    Then the command output should contain "remember/pulled_DEV.jsonl"
    And the command returncode is "0"
    When I run "bubble3 export -r pulled -kvp -f tab -c keyA,keyB,keyC.1,keyC.2,keyC.3.keyDinList -a 10"
    Then the command returncode is "0"
    And the command output should contain
      """
      BUBBLE_IDX|keyA|keyB|keyC.1|keyC.2|keyC.3.keyDinList
      ----------|----|----|------|------|-----------------
      0         |A_0 |B_0 |c     |66    |D_0
      1         |A_1 |B_1 |c     |66    |D_1
      2         |A_2 |B_2 |c     |66    |D_2
      3         |A_3 |B_3 |c     |66    |D_3
      4         |A_4 |B_4 |c     |66    |D_4
      5         |A_5 |B_5 |c     |66    |D_5
      6         |A_6 |B_6 |c     |66    |D_6
      7         |A_7 |B_7 |c     |66    |D_7
      8         |A_8 |B_8 |c     |66    |D_8
      9         |A_9 |B_9 |c     |66    |D_9
      """
    When I run "bubble3 export -r pulled -kvp -f tab -c keyA,keyB,keyC.1,keyC.2,keyC.3.keyDinList -i 990 -a 10"
    Then the command returncode is "0"
    And the command output should contain
      """
      BUBBLE_IDX|keyA |keyB |keyC.1|keyC.2|keyC.3.keyDinList
      ----------|-----|-----|------|------|-----------------
      990       |A_990|B_990|c     |66    |D_990            
      991       |A_991|B_991|c     |66    |D_991            
      992       |A_992|B_992|c     |66    |D_992            
      993       |A_993|B_993|c     |66    |D_993            
      994       |A_994|B_994|c     |66    |D_994            
      995       |A_995|B_995|c     |66    |D_995            
      996       |A_996|B_996|c     |66    |D_996            
      997       |A_997|B_997|c     |66    |D_997            
      998       |A_998|B_998|c     |66    |D_998            
      999       |A_999|B_999|c     |66    |D_999         
      """
