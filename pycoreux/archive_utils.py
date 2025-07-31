"""
Archive and compression utilities.
"""

import bz2
import gzip
import lzma
import tarfile
import zipfile
from pathlib import Path
from typing import List, Optional, Union


class ArchiveUtils:
    """Utilities for working with archives and compressed files."""

    @staticmethod
    def tar_create(
        archive_path: Union[str, Path],
        files: List[Union[str, Path]],
        compression: Optional[str] = None,
    ) -> None:
        """
        Create tar archive (like tar command).

        Args:
            archive_path: Path for the new archive
            files: List of files/directories to include
            compression: Compression type ('gz', 'bz2', 'xz') or None
        """
        mode = "w"
        if compression == "gz":
            mode = "w:gz"
        elif compression == "bz2":
            mode = "w:bz2"
        elif compression == "xz":
            mode = "w:xz"

        with tarfile.open(str(archive_path), mode) as tar:
            for file_path in files:
                tar.add(str(file_path), arcname=Path(file_path).name)

    @staticmethod
    def tar_extract(
        archive_path: Union[str, Path], extract_to: Union[str, Path] = "."
    ) -> str:
        """
        Extract tar archive.

        Args:
            archive_path: Path to the archive
            extract_to: Directory to extract to

        Returns:
            String containing extracted files (one per line)
        """
        extracted_files = []

        with tarfile.open(str(archive_path), "r:*") as tar:
            tar.extractall(str(extract_to))
            extracted_files = tar.getnames()

        return "\n".join(extracted_files)

    @staticmethod
    def tar_list(archive_path: Union[str, Path]) -> List[dict]:
        """
        List contents of tar archive.

        Args:
            archive_path: Path to the archive

        Returns:
            List of file information dictionaries
        """
        files_info = []

        with tarfile.open(str(archive_path), "r:*") as tar:
            for member in tar.getmembers():
                files_info.append(
                    {
                        "name": member.name,
                        "size": member.size,
                        "is_file": member.isfile(),
                        "is_dir": member.isdir(),
                        "mode": oct(member.mode) if member.mode else None,
                        "mtime": member.mtime,
                    }
                )

        return files_info

    @staticmethod
    def zip_create(
        archive_path: Union[str, Path],
        files: List[Union[str, Path]],
        compression_level: int = 6,
    ) -> None:
        """
        Create zip archive.

        Args:
            archive_path: Path for the new archive
            files: List of files/directories to include
            compression_level: Compression level (0-9)
        """
        with zipfile.ZipFile(
            archive_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=compression_level,
        ) as zf:
            for file_path in files:
                path_obj = Path(file_path)
                if path_obj.is_file():
                    zf.write(file_path, path_obj.name)
                elif path_obj.is_dir():
                    for item in path_obj.rglob("*"):
                        if item.is_file():
                            arcname = item.relative_to(path_obj.parent)
                            zf.write(item, arcname)

    @staticmethod
    def zip_extract(
        archive_path: Union[str, Path], extract_to: Union[str, Path] = "."
    ) -> str:
        """
        Extract zip archive.

        Args:
            archive_path: Path to the archive
            extract_to: Directory to extract to

        Returns:
            String containing extracted files (one per line)
        """
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(extract_to)
            return "\n".join(zf.namelist())

    @staticmethod
    def zip_list(archive_path: Union[str, Path]) -> List[dict]:
        """
        List contents of zip archive.

        Args:
            archive_path: Path to the archive

        Returns:
            List of file information dictionaries
        """
        files_info = []

        with zipfile.ZipFile(archive_path, "r") as zf:
            for info in zf.infolist():
                files_info.append(
                    {
                        "name": info.filename,
                        "size": info.file_size,
                        "compressed_size": info.compress_size,
                        "is_dir": info.is_dir(),
                        "date_time": info.date_time,
                    }
                )

        return files_info

    @staticmethod
    def gzip_file(
        file_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None
    ) -> str:
        """
        Compress file with gzip.

        Args:
            file_path: File to compress
            output_path: Output file path (defaults to file_path.gz)

        Returns:
            Path to compressed file
        """
        if output_path is None:
            output_path = f"{file_path}.gz"

        with open(file_path, "rb") as f_in:
            with gzip.open(output_path, "wb") as f_out:
                f_out.writelines(f_in)

        return str(output_path)

    @staticmethod
    def gunzip_file(
        file_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None
    ) -> str:
        """
        Decompress gzip file.

        Args:
            file_path: Gzipped file to decompress
            output_path: Output file path (defaults to file_path without .gz)

        Returns:
            Path to decompressed file
        """
        if output_path is None:
            path_str = str(file_path)
            if path_str.endswith(".gz"):
                output_path = path_str[:-3]
            else:
                output_path = f"{path_str}.decompressed"

        with gzip.open(file_path, "rb") as f_in:
            with open(output_path, "wb") as f_out:
                f_out.writelines(f_in)

        return str(output_path)

    @staticmethod
    def compress_file(file_path: Union[str, Path], method: str = "gz") -> str:
        """
        Compress file using specified method.

        Args:
            file_path: File to compress
            method: Compression method ('gz', 'bz2', 'xz')

        Returns:
            Path to compressed file
        """
        output_path = f"{file_path}.{method}"

        with open(file_path, "rb") as f_in:
            if method == "gz":
                with gzip.open(output_path, "wb") as f_out:
                    f_out.writelines(f_in)
            elif method == "bz2":
                with bz2.open(output_path, "wb") as f_out:
                    f_out.writelines(f_in)
            elif method == "xz":
                with lzma.open(output_path, "wb") as f_out:
                    f_out.writelines(f_in)
            else:
                raise ValueError(f"Unsupported compression method: {method}")

        return output_path

    @staticmethod
    def decompress_file(file_path: Union[str, Path]) -> str:
        """
        Auto-detect and decompress file.

        Args:
            file_path: Compressed file to decompress

        Returns:
            Path to decompressed file
        """
        path_str = str(file_path)

        if path_str.endswith(".gz"):
            return ArchiveUtils.gunzip_file(file_path)
        elif path_str.endswith(".bz2"):
            output_path = path_str[:-4]
            with bz2.open(file_path, "rb") as f_in:
                with open(output_path, "wb") as f_out:
                    f_out.writelines(f_in)
            return output_path
        elif path_str.endswith(".xz"):
            output_path = path_str[:-3]
            with lzma.open(file_path, "rb") as f_in:
                with open(output_path, "wb") as f_out:
                    f_out.writelines(f_in)
            return output_path
        else:
            raise ValueError(f"Unknown compression format for: {file_path}")
