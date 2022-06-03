def test_article_folder_to_save_path_only_cat_and_title(article_md_saver):
    article_md_saver.article.meta.subcategory = None
    test_folder = article_md_saver.app_config.data_dir.joinpath(
        "Test category", "Test title"
    )
    folder = article_md_saver.folder_path
    assert folder == test_folder
