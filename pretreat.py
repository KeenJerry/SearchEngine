import doc_analyzer

if __name__ == "__main__":
	source_path = "../../one/"
	destination_path = "../TermResource/"
	doc_analyzer.read_data_from_path(source_path, destination_path)
	doc_analyzer.calc_idf(source_path, destination_path, destination_path)