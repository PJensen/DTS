
class DTS:
    def __init__(self, aDataType, aSize):
        self.DataType = aDataType
        self.Size = aSize

# "Schema" can be grabbed from an insert somewheres;
# starts with the first angle bracket; ends at the last bracket.
schema = """<ProdSubGroupCode, nvarchar(70),>
           ,<ProdSubGroupDesc, nvarchar(255),>
           ,<Level, numeric(18,0),>
           ,<ClientId, int,>
           ,<Add_Dt, datetime,>
           ,<Add_RepId, int,>
           ,<UpDate_Dt, datetime,>
           ,<UpDate_RepId, int,>
           ,<Inactive, bit,>"""

def translateDataType2DTS(dt):
    size_t = -1

    if (dt.find('char') != -1):
        if (len(dt.split('(')) > 0):
            size_t = int(dt.split('(')[1].split(')')[0].replace(' ', ''))            
        ret_t = 'String'
    elif (dt.find('int') != -1):
        ret_t = 'Int32'
    elif (dt.find('numeric') != -1):
        ret_t = 'Decimal'
    elif (dt.find('datetime') != -1):
        ret_t = 'DateTime'
    elif (dt.find('bit') != -1):
        ret_t = 'Boolean'
    elif (dt.find('decimal') != -1):
        ret_t = 'Double'
    elif (dt.find('text') != -1):
        ret_t = 'String'
    elif (dt.find('money') != -1):
        ret_t = 'Double'
    elif (dt.find('float') != -1):
        ret_t = 'Float'
        
    return DTS(ret_t, size_t)
            
    print('\n\n\n\n')

# Only spits out the meat code; not the fluff.
print('---------[ C# Code Section ]------\n\n')
for index in schema.split('<'):
    
    try:
        value = index.split('<')[0].split(',')[0].replace(' ', '')
        dataType = index.split('<')[0].split(',')[1].replace(' ', '')
    except:
        continue



    newDTS = translateDataType2DTS(dataType)

    codeLine = '/// <summary>\n'
    codeLine += '/// ' + value + '\n'

    if ('string' in newDTS.DataType.lower()):        
        codeLine += '/// <remarks>This field has a maximum length of ' + str(newDTS.Size) + ' characters.</remarks>\n'
    
    codeLine += '/// </summary>\n'
    codeLine += 'public virtual '
    
    codeLine += newDTS.DataType + ' ' + value

    codeLine += ' { get; set; }'
    print(codeLine + '\n')
    codeLine = ''

# Only spits out the meat hbXML; no fluff.
print('---------[ HBXML Section ]------\n\n')
for index in schema.split('<'):
    codeLine = '<property name="%s" column="%s" type="%s"'
    try:
        value = index.split('<')[0].split(',')[0].replace(' ', '')
        dataType = index.split('<')[0].split(',')[1].replace(' ', '')
    except:
        continue

    newDTS = translateDataType2DTS(dataType)
    if (newDTS.DataType != 'String'):
        codeLine = (codeLine % (value, value, newDTS.DataType)) + '/>'
    if (newDTS.DataType == 'String') and (newDTS.Size > 0):
        codeLine = (codeLine % (value, value, newDTS.DataType)) + ' length="%s"' % newDTS.Size + '/>'
    elif (newDTS.DataType == 'String'):
        codeLine = (codeLine % (value, value, newDTS.DataType)) + '/>'

    print(codeLine)
    codeLine = ''

# Only spits out the meat hbXML; no fluff.
print('-------------[ Auto Generated Sanity Code]--------------\n\n')
print('#region IDataAccessObject Members')
print('        /// <summary>')
print('        /// Check the field lengths for string based fields in this object.')
print('        /// </summary>')
print('        public void CheckFieldLengths()')
print('        {')


for index in schema.split('<'):
    try:
        value = index.split('<')[0].split(',')[0].replace(' ', '')
        dataType = index.split('<')[0].split(',')[1].replace(' ', '')
    except:
        continue

    newDTS = translateDataType2DTS(dataType)
    codeLine += newDTS.DataType + ' ' + value
    if (newDTS.DataType != 'String') and (newDTS.Size > 0):
        continue
    elif (newDTS.DataType != 'String'):
        continue
    
    if (newDTS.DataType == 'String') and (newDTS.Size > 0):
        print('            if (Util.chkLenExceeded(this.' + str(value) + ', ' + str(newDTS.Size) + '))')
        print('                Util.GenerateFieldLengthException("' +  value + '");')

print('        }')
print('#endregion')

        
