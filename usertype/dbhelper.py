import mysql.connector

# Written by Matthew Lukaszewski
# 4/2/22
# driver code for django interface

class ManagerException(Exception): # custom error, inherits from Exception, no further implemtation needed
    pass

class dbManager(object):

    def __init__(self, inHost='localhost', inAuthPlugin='mysql_native_password'):
        """
        :param inHost: destination of dtb for future connection (default to localhost)
        :param inAuthPlugin: plugin to use for collection to dtb (default to mysql_native_password)
        """
        self.__host = inHost
        self.__authPlugin = inAuthPlugin
        self.__dtbConnection = None
        self.__cursor = None

    def connect(self, inUserName, inPassword, inDatabase):
        """
        :param inUserName: username of mysql account
        :param inPassword: password of mysql account
        :param inDatabase: name of database for future queries
        :return: None
        """
        self.__dtbConnection = mysql.connector.connect(
            host=self.__host,
            user=inUserName,
            passwd=inPassword,
            auth_plugin=self.__authPlugin,
            database=inDatabase,
        )

    # Feature F1
    def getFeatureOne(self, inByName=False, inByDept=False, inBySalary=False):
        """
        :param inByName: optional parameter to specify sort by name
        :param inByDept: optional parameter to specify sort by dept
        :param inBySalary: optional parameter to specify sort by salary
        :return: resulting cursor
        """
        query = ""
        if (inByName):
            query = "select name from instructor order by name;"
        elif (inByDept):
            query = "select name from instructor order by dept_name;"
        elif (inBySalary):
            query = "select name from instructor order by salary;"

        if (query == ""):
            raise ManagerException("order by clause not specified in parameters")

        return self.__executeQuery(query)

    # Feature 2
    def getFeatureTwo(self):
        """
        :return: resulting cursor
        """
        query = "select dept_name, min(salary), max(salary), avg(salary) from instructor group by dept_name;"
        return self.__executeQuery(query)

    # Feature 3
    def getFeatureThree(self, inProfessor, inSemester):
        """
        :param inProfessor:
        :param inSemester:
        :return: resulting cursor
        """
        inSemester = str(inSemester)
        query = ("select name, dept_name, count(distinct takes.ID) as number_of_students from instructor inner " 
                 "join teaches on instructor.ID = teaches.ID inner join section on teaches.sec_id = section.sec_id "
                 "inner join takes on section.sec_id = takes.sec_id where takes.semester = '"+inSemester+"' and "
                 "name = '"+inProfessor+"';")
        return self.__executeQuery(query)

    #Feature 4
    def getFeatureFour(self, inProfessor, inSemester):
        """
        :param inProfessor:
        :return:
        """
        inSemester = str(inSemester)
        query = ("select instructor.name, teaches.course_id, teaches.sec_id, count(distinct takes.ID) as "
                 "number_of_students from teaches inner join instructor on teaches.id = instructor.id "
                 "inner join section on teaches.course_id = section.course_id inner join takes on "
                 "section.sec_id = takes.sec_id where instructor.name = '"+inProfessor+"' and teaches.semester = '"+inSemester+"';")
        return self.__executeQuery(query)

    # Feature 5
    def getFeatureFive(self, inProfessor, inSemester):
        """
        :param inProfessor:
        :param inSemester:
        :return:
        """
        inSemester = str(inSemester)
        query = ("select distinct student.name from student inner join takes on student.ID = takes.ID "
                 "inner join section on takes.course_id = section.course_id inner join teaches on "
                 "section.course_id = teaches.course_id inner join instructor on teaches.ID = instructor.ID "
                 "where instructor.name = '"+inProfessor+"' and teaches.semester = '"+inSemester+"';")
        return self.__executeQuery(query)

    #Feature 6
    def getFeatureSix(self, inDept, inSemester):
        """
        :param inDept:
        :param inSemester:
        :return:
        """
        inSemester = str(inSemester)
        query = "select course_id, sec_id from teaches where instr(course_id,'"+inDept+"') = 1 and semester = '"+inSemester+"' and year = 2019;"
        return self.__executeQuery(query)

    def __executeQuery(self, inQuery):
        """
        :param inQuery: string parameter to supply a sql statement
        :return: resulting cursor is returned
        """
        if (self.__dtbConnection == None):
            raise ManagerException("Database connection not opened")

        if (self.__cursor == None):
            self.__cursor = self.__dtbConnection.cursor()

        self.__cursor.execute(inQuery)
        return self.__cursor.fetchall()

    # def __del__(self):  # Destructor to close cursor and dtb connection
    #
    #     if (self.__cursor != None):
    #         self.__cursor.close()
    #
    #     if (self.__dtbConnection != None):
    #         self.__dtbConnection.close()
