# Create a GCS bucket

resource "google_storage_bucket" "source_code_bucket" {
    count = var.deploy_cf_flag ? 1 : 0
  name = "source-code-${var.project_id}"
  location = var.region

}

# Zip Each Directory in cf_src
data "archive_file" "zip_cf_src" {
    for_each = var.deploy_cf_flag ? local.cloud_functions : {}
    type = "zip"
    source_dir = "${path.module}/cf_src/${each.key}/"
    output_path = "${path.module}/artifacts/${each.key}"
}


# Upload the zip file to the GCS bucket

resource "google_storage_bucket_object" "zipped_data" {
    for_each = var.deploy_cf_flag ? local.cloud_functions : {}
    name = format("%s-%s.zip", each.key, data.archive_file.zip_cf_src[each.key].output_md5)
    bucket = google_storage_bucket.source_code_bucket[0].bucket_name
    source = data.archive_file.zip_cf_src[each.key].output_path

    depends_on = [ google_storage_bucket.source_code_bucket ]
} 

 