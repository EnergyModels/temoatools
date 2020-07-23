## Instructions to verify temoa_stochastic performance
The instance of temoa_stochastic was verified by comparing it against the performance of the latest version of temoa for a known dataset.

###Prerequisites:
1) Install temoa and temoatools
    - follow instructions in temoatools/README.md
    - verification was performed with temoa commit 9d10c1da81dc6b4f2b34cadfac9db947251254e2, https://github.com/TemoaProject/temoa/tree/9d10c1da81dc6b4f2b34cadfac9db947251254e2
    - place temoa folder within temoatools/projects/verify_temoa_stochastic
        - If this is not done, then the paths will need to be updated in the configuration files
         
2) Install temoa_stochastic
    - follow instructions in temoatools/projects/puerto_rico_stoch/README.md
    - This is the version of temoa used for the Puerto Rico project
    - make note of the path to temoa_stochastic
### Run the test cases
1) run test cases with the current version of temoa
2) run test cases with the stochastic version of temoa
    
Sample code in Anaconda3 (for running the current version of temoa):

>
    cd temoatools/projects/verify_temoa_stochastic
    git clone https://github.com/TemoaProject/temoa
    cd temoa
    git checkout 9d10c1da81dc6b4f2b34cadfac9db947251254e2
    
    conda activate temoa-py3
    python temoa_model/ --config=../current/config_NGCC.txt
    python temoa_model/ --config=../current/config_solarBatt.txt
    python temoa_model/ --config=../current/config_Base_zeroDR.txt

Sample code in Anaconda2 (for running stochastic version):
    
    conda activate temoa-stoch-py2
    cd temoatools/temoa_stochastic
    python temoa_model/ --config=../projects/verify_temoa_stochastic/stochastic/config_NGCC.txt
    python temoa_model/ --config=../projects/verify_temoa_stochastic/stochastic/config_solarBatt.txt
    python temoa_model/ --config=../projects/verify_temoa_stochastic/stochastic/config_Base_zeroDR.txt    
