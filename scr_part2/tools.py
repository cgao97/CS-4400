import tkinter.messagebox as Msgbox

def strToDate(date, cursor):
    cmd = "SELECT STR_TO_DATE('" + date + "', '%m/%d/%Y')"
    cursor.execute(cmd)
    result = cursor.fetchall()
    result = list(map(lambda x: x[0], result))[0]
    if not result:
        Msgbox.showerror("Error", "Date Error")
        return ""
    return result

def dateToStr(date, cursor):
    cmd = "SELECT DATE_FORMAT ('" + date + "', '%m/%d/%Y')"
    cursor.execute(cmd)
    result = cursor.fetchall()
    result = list(map(lambda x: x[0], result))[0]
    return result