import cgi

form = cgi.FieldStorage()
pause = form.getfirst("pause", 3)
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>It was inputed in form</title>
        </head>
        <body>""")

print("<h1>It was inputed</h1>")
print("<p>pause: {}</p>".format(pause))

print("""</body>
        </html>""")
# with open('presult', 'w', encoding="utf-8") as f:
#     print(pause, file=f)
#
# import wf
