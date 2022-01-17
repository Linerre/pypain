-- Author: Leon Lin zl37@nyu.edu
-- Last Modified: 2022-01-16 Mon

--[[ Copy content from Google Sheet consective cells 
	and paste it to ARES form on a single operation.
	
    For example, the following is a typical row on AA's textbook list
   ----------------------------------------------------------------------
   | title  | author | ISBN | publisher | edition | ?print or electronic|
   ----------------------------------------------------------------------
   ----1--------2--------3--------4----------5----------6------------------
--]]

--[[ 
	1. Copy the row and then get a tab delimited string:
		title\tauthor\tISBN\tpublisher\tedition\tprint?
	2. Split the string and store each components in a table:
		{'title', 'author', 'ISXN' .... }
	3. Use SetFieldValue method to set the field value accordingly
--]]


-- Import .NET libs for access to Windows clipboard.
luanet.load_assembly("System.Windows.Forms")
local Clipboard = luanet.import_type("System.Windows.Forms.Clipboard")
local Application = luanet.import_type("System.Windows.Forms.Application")
local File = luanet.import_type("System.IO.File")


-- In settings.<setting_name>, <setting_name> is defined in the ./Config.xml
-- GetSetting is a method provided by ARES for acquiring <setting_name>
local interfaceMngr = nil
local copyFromSheets = {}
copyFromSheets.RibbonPage = nil
copyFromSheets.Button = nil

local settings = {}
settings.Autofilling = GetSetting("Autofilling")

-- Init function to control the processes after opening an item
function Init()
    if settings.Autofilling then
		interfaceMngr = GetInterfaceManager()
		
		-- create the ribbonpage (a label next to the "Home" on top right)
		copyFromSheets.RibbonPage = interfaceMngr:CreateRibbonPage("My Buttons")
		
		-- add a button to get the clipboard content
		copyFromSheets.Button = copyFromSheets.RibbonPage:CreateButton("Paste", GetClientImage("Paste32"), "Fill", "My Buttons")
		
    end
end

-- Fill the citation fields
function Fill()
	local copied = Clipboard.GetText()
	local citation = Spliter(copied, "\t")
	-- local content = File.ReadAllText("C:\\Users\\zl37\\Documents\\Ares\\Addons\\CopyFromSheets\\test.txt");
    
	if ((GetFieldValue("Item", "Title") == nil) or (GetFieldValue("Item", "Title") == null) or (GetFieldValue("Item", "Title") == "")) then
        SetFieldValue("Item", "Title", citation[1])
		SetFieldValue("Item", "ISXN", citation[2])
		SetFieldValue("Item", "Author", citation[3])
		SetFieldValue("Item", "Publisher", citation[4])
		SetFieldValue("Item", "Edition", citation[5])
    end
	Posthook()
end

-- Split string in clipboard
function Spliter(bookinfo, delimiter)
	-- in case there is no delimiter provided when calling the function 
	if delimiter == nil then
		delimiter = "\t"
	end
	
	-- title, ISBN, author, publisher, edition
	--[[ local citation = {
		["title"] = "";
		["ISXN"] = "";
		["author"] = "";
		["publisher"] = "";
		["edition"] = "";
	}; 
	--]]

	local result = {};
	
	for match in string.gmatch(bookinfo, "[^"..delimiter.."]+") do
		table.insert(result, match)
	end
	
	return result

end

-- Post hook to check empty fields and fill them in with "n/a".
function Posthook()
	local checklist = {
		["title"] = "Title", 
		["ixbn"] = "ISXN", 
		["author"] = "Author", 
		["publisher"] = "Publisher", 
		["edition"] = "Edition", 
		["pubdate"] = "PubDate"
	}
	
	for _, item in pairs(checklist) do
		if ((GetFieldValue("Item", item) == nil) or (GetFieldValue("Item", item) == null) or (GetFieldValue("Item", item) == "")) then
			SetFieldValue("Item", item, "N/A")
		end
	end
end

-- TODO
-- Add function to also handle ebook url as well as textbook? field
