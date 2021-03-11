build:
	@echo "Building mbr_info..."
	@cp main.py mbr_info
	@chmod +x mbr_info
	@echo "...Done building"

clean:
	@echo "Deleting mbr_info executable and md5 and sha1 files..."
	@rm mbr_info
	@rm MD5-*.txt
	@rm SHA1-*.txt
	@echo "...Done cleaning"