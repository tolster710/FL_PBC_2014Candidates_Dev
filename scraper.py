### Made by TOlly 8/8/14
### Parses palm beach county Qualified candidates


import scraperwiki, lxml.html, re, datetime


def scrapePage(url):
    html = None
    attempts = 0
    
    while html == None and attempts <3:
        try:
            html= scraperwiki.scrape(url)
        except:
            attempts += 1
            continue
        if html == None and attempts == 3:
            print log("no dice")
    return html

def parse_html(html_in):
    #page_html=scrapePage()
    page_index_tree = lxml.html.fromstring(html_in)
    #below correcting for removed breaks in formatted string
    for br in page_index_tree.xpath("*//br"):
        br.tail = ", " + br.tail if br.tail else ", "
    candidate_section=page_index_tree.cssselect('div#OfficeCandidate')[0]
    data={}
    discard_data=True
    Election=candidate_section.cssselect('span#lblElection')
    candidate_name=candidate_section.cssselect('span#lblName')
    if candidate_name[0].text_content() == '':
        return (False)
    else:
        if Election:
            data['Election']=Election[0].text_content()
        Office=candidate_section.cssselect('span#lblOffice')
        if Office:
            data['Office']=Office[0].text_content()
        candidate_name=candidate_section.cssselect('span#lblName')
        if candidate_name:
            data['Candidate_Name']=candidate_name[0].text_content()
            discard_data=False
        candidate_party=candidate_section.cssselect('span#lblParty')
        if candidate_party:
            data['Party']=candidate_party[0].text_content()
        candidate_addr=candidate_section.cssselect('span#lblFullAddress')
        if candidate_addr:
            data['Address']=candidate_addr[0].text_content()
        candidate_Bus_phone=candidate_section.cssselect('span#lblBusinessPhone')
        if candidate_Bus_phone:
            data['Phone']=candidate_Bus_phone[0].text_content()
        candidate_website=candidate_section.cssselect('span#lblWebsite')
        if candidate_website:
            data['Website']=candidate_website[0].text_content()
        candidate_announce_date=candidate_section.cssselect('span#lblannounceddate')
        if candidate_announce_date:
            data['Announced']=candidate_announce_date[0].text_content()
        candidate_won=candidate_section.cssselect('span#lblWon')
        if candidate_won:
            data['Won']=candidate_won[0].text_content()
        candidate_status=candidate_section.cssselect('span#lblCandidateElectionStatus')
        if candidate_status:
            data['Status']=candidate_status[0].text_content()
        del_list=[]
        for key in data:
            if data[key]=='':
                del_list.append(key)
        for k in del_list:
            del data[k]
        if len(data)<3:
            discard_data=True
        if discard_data:
            return(False)
        else:
            return(data)


#main execution

eid=123
oid=400
cid=100
for _oid in range(oid,800):
    for _cid in range(cid,400):
        url = 'http://www.pbcelections.org/OfficeCandidate.aspx?eid=123&oid=%s&cid=%s'%(_oid,_cid)
        data=parse_html(scrapePage(url))
        if data:
            #print "We got something!"
            scraperwiki.sqlite.save(['Candidate_Name'], data, table_name='Candidates')
        else:
            #print "We got nothin"
