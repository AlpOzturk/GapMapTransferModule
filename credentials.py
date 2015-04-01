
DATABASE_URI = 'postgres://wgoaxzvjxecwat:g147MYb5i1bN6AMW-JHaF1Y4b1@ec2-54-163-234-163.compute-1.amazonaws.com:5432/dfp2icp48dku49'
DATABASE_KEY =  'g147MYb5i1bN6AMW-JHaF1Y4b1'

# Working SCP cmd: scp -C -i .ssh/gapmap-azure.key ubuntu@gapmap.cloudapp.net:/home/ubuntu/alp_test_folder/scp_test.txt .
SCP_ARGS = ['scp', '-C', '-i', '/home/mobaxterm/.ssh/gapmap-azure.key', 'ubuntu@gapmap.cloudapp.net:/home/ubuntu/alp_test_folder/', '.']