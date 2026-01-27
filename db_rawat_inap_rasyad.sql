-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 26, 2026 at 03:39 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_rawat_inap_rasyad`
--

-- --------------------------------------------------------

--
-- Table structure for table `kamar_rasyad`
--

CREATE TABLE `kamar_rasyad` (
  `id_kamar_rasyad` int(11) NOT NULL,
  `no_kamar_rasyad` varchar(10) NOT NULL,
  `kelas_rasyad` varchar(20) DEFAULT NULL,
  `status_kamar_rasyad` varchar(20) DEFAULT 'Kosong',
  `harga_rasyad` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `nama_kamar` varchar(100) DEFAULT NULL,
  `harga_kamar` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kamar_rasyad`
--

INSERT INTO `kamar_rasyad` (`id_kamar_rasyad`, `no_kamar_rasyad`, `kelas_rasyad`, `status_kamar_rasyad`, `harga_rasyad`, `created_at`, `nama_kamar`, `harga_kamar`) VALUES
(1, '101', 'VIP', 'Terisi', 500000.00, '2026-01-26 01:34:26', NULL, NULL),
(2, '102', 'VIP', 'Kosong', 500000.00, '2026-01-26 01:34:26', NULL, NULL),
(3, '201', 'Kelas 1', 'Terisi', 300000.00, '2026-01-26 01:34:26', NULL, NULL),
(4, '202', 'Kelas 1', 'Kosong', 300000.00, '2026-01-26 01:34:26', NULL, NULL),
(5, '301', 'Kelas 2', 'Terisi', 150000.00, '2026-01-26 01:34:26', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `pasien_rasyad`
--

CREATE TABLE `pasien_rasyad` (
  `id_pasien_rasyad` int(11) NOT NULL,
  `nama_rasyad` varchar(100) NOT NULL,
  `alamat_rasyad` text DEFAULT NULL,
  `kontak_rasyad` varchar(15) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pasien_rasyad`
--

INSERT INTO `pasien_rasyad` (`id_pasien_rasyad`, `nama_rasyad`, `alamat_rasyad`, `kontak_rasyad`, `created_at`) VALUES
(1, 'Dani', 'Jl. Blok M No. 321, Jakarta', '081234567890', '2026-01-26 01:34:25'),
(2, 'Iting', 'Jl. Moh Toha No. 54, Bandung', '082345678901', '2026-01-26 01:34:25'),
(3, 'Gavin', 'Jl. Dipenogoro No. 67, Surabaya', '083456789012', '2026-01-26 01:34:25'),
(4, 'Aripin', 'Jl. Tugu No. 89, Medan', '084567890123', '2026-01-26 01:34:25'),
(5, 'Grandy', 'Jl. Malioboro No. 101, Yogyakarta', '085678901234', '2026-01-26 01:34:25');

-- --------------------------------------------------------

--
-- Table structure for table `rawat_inap_rasyad`
--

CREATE TABLE `rawat_inap_rasyad` (
  `id_rawat_rasyad` int(11) NOT NULL,
  `id_pasien_rasyad` int(11) NOT NULL,
  `id_kamar_rasyad` int(11) NOT NULL,
  `tgl_masuk_rasyad` date NOT NULL,
  `tgl_keluar_rasyad` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `tgl_masuk` date DEFAULT NULL,
  `tgl_keluar` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rawat_inap_rasyad`
--

INSERT INTO `rawat_inap_rasyad` (`id_rawat_rasyad`, `id_pasien_rasyad`, `id_kamar_rasyad`, `tgl_masuk_rasyad`, `tgl_keluar_rasyad`, `created_at`, `tgl_masuk`, `tgl_keluar`) VALUES
(1, 1, 1, '2026-01-10', '2026-01-15', '2026-01-26 01:34:26', NULL, NULL),
(2, 2, 3, '2026-01-12', '2026-01-18', '2026-01-26 01:34:26', NULL, NULL),
(3, 3, 5, '2026-01-14', NULL, '2026-01-26 01:34:26', NULL, NULL),
(4, 4, 2, '2026-01-16', NULL, '2026-01-26 01:34:26', NULL, NULL),
(5, 5, 4, '2026-01-17', '2026-01-19', '2026-01-26 01:34:26', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_rasyad`
--

CREATE TABLE `transaksi_rasyad` (
  `id_transaksi_rasyad` int(11) NOT NULL,
  `id_pasien_rasyad` int(11) NOT NULL,
  `id_rawat_rasyad` int(11) DEFAULT NULL,
  `total_biaya_rasyad` decimal(10,2) DEFAULT NULL,
  `status_pembayaran_rasyad` varchar(20) DEFAULT 'Belum Bayar',
  `tgl_rasyad` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi_rasyad`
--

INSERT INTO `transaksi_rasyad` (`id_transaksi_rasyad`, `id_pasien_rasyad`, `id_rawat_rasyad`, `total_biaya_rasyad`, `status_pembayaran_rasyad`, `tgl_rasyad`, `created_at`) VALUES
(1, 1, 1, 2500000.00, 'Lunas', '2026-01-15', '2026-01-26 01:34:26'),
(2, 2, 2, 1800000.00, 'Lunas', '2026-01-18', '2026-01-26 01:34:26'),
(3, 3, 3, 1500000.00, 'Belum Bayar', '2026-01-19', '2026-01-26 01:34:26'),
(4, 4, 4, 1000000.00, 'Belum Bayar', '2026-01-19', '2026-01-26 01:34:26'),
(5, 5, 5, 750000.00, 'Sudah Bayar', '2026-01-19', '2026-01-26 01:34:26'),
(6, 3, 1, 99999999.99, 'Belum Lunas', '2026-01-26', '2026-01-26 01:40:10'),
(7, 2, 1, 20000000.00, 'Lunas', '2026-01-23', '2026-01-26 01:43:05');

-- --------------------------------------------------------

--
-- Table structure for table `user_rasyad`
--

CREATE TABLE `user_rasyad` (
  `id_user_rasyad` int(11) NOT NULL,
  `username_rasyad` varchar(50) NOT NULL,
  `password_rasyad` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_rasyad`
--

INSERT INTO `user_rasyad` (`id_user_rasyad`, `username_rasyad`, `password_rasyad`, `created_at`) VALUES
(1, 'admin', 'admin123', '2026-01-26 01:34:25'),
(2, 'petugas1', 'petugas123', '2026-01-26 01:34:25'),
(3, 'petugas2', 'petugas123', '2026-01-26 01:34:25'),
(4, 'keuangan', 'keuangan123', '2026-01-26 01:34:25'),
(5, 'dokter', 'dokter123', '2026-01-26 01:34:25');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kamar_rasyad`
--
ALTER TABLE `kamar_rasyad`
  ADD PRIMARY KEY (`id_kamar_rasyad`),
  ADD UNIQUE KEY `no_kamar_rasyad` (`no_kamar_rasyad`);

--
-- Indexes for table `pasien_rasyad`
--
ALTER TABLE `pasien_rasyad`
  ADD PRIMARY KEY (`id_pasien_rasyad`);

--
-- Indexes for table `rawat_inap_rasyad`
--
ALTER TABLE `rawat_inap_rasyad`
  ADD PRIMARY KEY (`id_rawat_rasyad`),
  ADD KEY `id_pasien_rasyad` (`id_pasien_rasyad`),
  ADD KEY `id_kamar_rasyad` (`id_kamar_rasyad`);

--
-- Indexes for table `transaksi_rasyad`
--
ALTER TABLE `transaksi_rasyad`
  ADD PRIMARY KEY (`id_transaksi_rasyad`),
  ADD KEY `id_pasien_rasyad` (`id_pasien_rasyad`),
  ADD KEY `id_rawat_rasyad` (`id_rawat_rasyad`);

--
-- Indexes for table `user_rasyad`
--
ALTER TABLE `user_rasyad`
  ADD PRIMARY KEY (`id_user_rasyad`),
  ADD UNIQUE KEY `username_rasyad` (`username_rasyad`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kamar_rasyad`
--
ALTER TABLE `kamar_rasyad`
  MODIFY `id_kamar_rasyad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `pasien_rasyad`
--
ALTER TABLE `pasien_rasyad`
  MODIFY `id_pasien_rasyad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `rawat_inap_rasyad`
--
ALTER TABLE `rawat_inap_rasyad`
  MODIFY `id_rawat_rasyad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `transaksi_rasyad`
--
ALTER TABLE `transaksi_rasyad`
  MODIFY `id_transaksi_rasyad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_rasyad`
--
ALTER TABLE `user_rasyad`
  MODIFY `id_user_rasyad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rawat_inap_rasyad`
--
ALTER TABLE `rawat_inap_rasyad`
  ADD CONSTRAINT `rawat_inap_rasyad_ibfk_1` FOREIGN KEY (`id_pasien_rasyad`) REFERENCES `pasien_rasyad` (`id_pasien_rasyad`),
  ADD CONSTRAINT `rawat_inap_rasyad_ibfk_2` FOREIGN KEY (`id_kamar_rasyad`) REFERENCES `kamar_rasyad` (`id_kamar_rasyad`);

--
-- Constraints for table `transaksi_rasyad`
--
ALTER TABLE `transaksi_rasyad`
  ADD CONSTRAINT `transaksi_rasyad_ibfk_1` FOREIGN KEY (`id_pasien_rasyad`) REFERENCES `pasien_rasyad` (`id_pasien_rasyad`),
  ADD CONSTRAINT `transaksi_rasyad_ibfk_2` FOREIGN KEY (`id_rawat_rasyad`) REFERENCES `rawat_inap_rasyad` (`id_rawat_rasyad`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
