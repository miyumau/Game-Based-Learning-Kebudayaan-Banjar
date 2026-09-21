// tombol lanjut setelah materi rumah bubungan tinggi
function lanjut() {
  let kotak_materi1 = document.querySelector("#materi1");
  let kotak_materi2 = document.querySelector("#materi2");
  if (kotak_materi1.style.display === "block") {
    kotak_materi1.style.display = "none";
    kotak_materi2.style.display = "block";
  }
}
// tombol kembali setelah materi rumah bubungan tinggi
function kembali() {
  let kotak_materi1 = document.querySelector("#materi1");
  let kotak_materi2 = document.querySelector("#materi2");
  if (kotak_materi2.style.display === "block") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}

// tombol lanjut setelah materi rumah balai bini
function lanjut2() {
  let kotak_materi1 = document.querySelector("#materi2");
  let kotak_materi2 = document.querySelector("#materi3");
  if (kotak_materi1.style.display === "block") {
    kotak_materi1.style.display = "none";
    kotak_materi2.style.display = "block";
  }
}
// tombol kembali setelah materi rumah balai bini
function kembali2() {
  let kotak_materi1 = document.querySelector("#materi2");
  let kotak_materi2 = document.querySelector("#materi3");
  if (kotak_materi2.style.display === "block") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}

// tombol lanjut setelah materi rumah balai laki
function lanjut3() {
  let kotak_materi1 = document.querySelector("#materi3");
  let kotak_materi2 = document.querySelector("#materi4");
  if (kotak_materi1.style.display === "block") {
    kotak_materi1.style.display = "none";
    kotak_materi2.style.display = "block";
  }
}
// tombol kembali setelah materi rumah balai laki
function kembali3() {
  let kotak_materi1 = document.querySelector("#materi3");
  let kotak_materi2 = document.querySelector("#materi4");
  if (kotak_materi2.style.display === "block") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}

// tombol lanjut setelah materi rumah ...
function lanjut4() {
  let kotak_materi1 = document.querySelector("#materi4");
  let kotak_materi2 = document.querySelector("#materi5");
  if (kotak_materi1.style.display === "block") {
    kotak_materi1.style.display = "none";
    kotak_materi2.style.display = "block";
  }
}
// tombol kembali setelah materi rumah ....
function kembali4() {
  let kotak_materi1 = document.querySelector("#materi4");
  let kotak_materi2 = document.querySelector("#materi5");
  if (kotak_materi2.style.display === "block") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}

// buat menghilangkan tombol game dan materi agar profil user kelihatan
function profil() {
  let tulisan = document.querySelector("#tulisantema");

  let buat_profil = document.querySelector(".buat_profil");
  if (tulisan.style.display === "block") {
    tulisan.style.display = "none";

    buat_profil.style.display = "block";
  } else {
    tulisan.style.display = "block";

    buat_profil.style.display = "none";
  }
}

function penjelasan() {
  let kotak_game = document.querySelector(".kotak_materi_diatas");
  let kotak_materi_panjang = document.querySelector(".kotak_materi_panjang");
  let kotak_materi_panjang2 = document.querySelector("#kotak_materi_2");
  let kotak_materi_panjang3 = document.querySelector("#kotak_materi_3");
  let buat_profil = document.querySelector(".buat_profil");
  if (kotak_game.style.display === "block") {
    kotak_game.style.display = "none";
    kotak_materi_panjang.style.display = "none";
    kotak_materi_panjang2.style.display = "none";
    kotak_materi_panjang3.style.display = "none";
    buat_profil.style.display = "block";
  } else {
    kotak_game.style.display = "block";
    kotak_materi_panjang.style.display = "block";
    kotak_materi_panjang2.style.display = "block";
    kotak_materi_panjang3.style.display = "block";
    buat_profil.style.display = "none";
  }
}

function soal_lanjut() {
  let kotak_materi1 = document.querySelector(".quiz-container");
  let kotak_materi2 = document.querySelector(".container-cerita");
  if (kotak_materi1.style.display === "none") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}

function soal_lanjut1() {
  let kotak_materi1 = document.querySelector(".card");
  let kotak_materi2 = document.querySelector(".container-cerita");
  if (kotak_materi1.style.display === "none") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}

function soal_lanjut2() {
  let kotak_materi1 = document.querySelector("#board");
  let kotak_materi2 = document.querySelector(".container-cerita");
  if (kotak_materi1.style.display === "none") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}

function soal_lanjut3() {
  let kotak_materi1 = document.querySelector("#board");
  let kotak_materi2 = document.querySelector(".container-cerita");
  if (kotak_materi1.style.display === "none") {
    kotak_materi2.style.display = "none";
    kotak_materi1.style.display = "block";
  }
}
