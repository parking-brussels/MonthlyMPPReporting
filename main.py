#!/opt/scripts/bin/launch.sh -e mpp
# Script to create and send monthly MPP reports to the MPP

# main script
import datetime

from excelfile import ExcelFile
from mail import Mail
from mpp import MPPList, MPP



def createBody():
    return """
<HTML>
	<p> Hello, </p>
	<p> In attachment you will find the transactions known by us in the system, could you
		please confirm and make the payment or inform us about the differences. </p>
	<p> Regards, </p>
	<p class=MsoNormal>
		<b>
			<span lang=NL-BE style='color:#1F497D;mso-fareast-language:FR-BE'>Vincent De Bie<o:p/>
			</span>
		</b>
	</p>
	<p class=MsoNormal>
		<b>
			<span lang=NL-BE style='color:#1F497D;mso-fareast-language:FR-BE'>IT Manager<o:p/>
			</span>
		</b>
	</p>
	<p class=MsoNormal>
		<span lang=FR-BE style='color:#1F497D;mso-fareast-language:NL-BE'>
			<a href="mailto:vdebie@parking.brussels">
				<span style='color:#1F497D'>vdebie@parking.brussels</span>
			</a>
			<o:p/>
		</span>
	</p>
</HTML>
    """


if __name__ == '__main__':

    # First day of previous month
    # Calculated as beginning of this month minus 1 day, and take first day of that month)
    Month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

    for mpp in MPPList(Month).list:
        file = ExcelFile(mpp)
        file.AddData()
        Mail(_email=mpp.GetEmail(),
             _attachments=[file.filename],
             _body=createBody(),
             _subject="Overview of the tickets of last month",
             _bcc="vdebie@parking.brussels",
             ).setSender("ICT-service", "ict@parking.brussels").send()
