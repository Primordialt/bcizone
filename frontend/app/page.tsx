import Link from "next/link";

import {
  PublicSiteAssets,
  PublicSiteFooter,
  PublicSiteHeader,
  PublicSiteScripts,
} from "./public-site-chrome";

export default function HomePage() {
  return (
    <>
      <PublicSiteAssets />

      <main className="page-wrapper">
        <PublicSiteHeader variant="dark" />

        <section className="overflow-hidden pt-5 pb-1 bg-dark dd-bg">
          <div className="container pt-3 pt-sm-4 pt-xl-5">
            <div className="row">
              <div className="col-md-6 d-flex flex-column mt-md-4 pt-5 pb-3 pb-sm-4 py-md-5">
                <h1 className="display-5 pb-3 text-white">Smart Loans for Every Need</h1>
                <p className="fs-3 text-start text-md-start pb-2 pb-md-3 mb-3 text-white">At <strong>BCI</strong>, we make financing simple and accessible. We’ve got you covered with flexible terms and quick approvals.</p>
                <div className="d-md-flex align-items-md-start">
                  <Link href="/register" className="btn btn-info flex-shrink-0 me-md-4 mb-md-0 mb-sm-4 mb-3 rounded-pill">Get a Loan Today</Link>
                </div>
                <div className="d-flex align-items-center justify-content-center justify-content-md-start text-start pt-4 pt-lg-5 mt-xxl-5">
                  <div className="text-light">400k+ users already with us</div>
                </div>
              </div>
              <div className="col-md-6 text-md-end text-center pt-5">
                <img src="/assets/images/section_111.png" style={{ maxWidth: "100%", height: "auto" }} alt="Hero" />
              </div>
            </div>
          </div>
        </section>

        <section className="container py-5 mt-md-3 my-lg-5">
          <div className="row"><div className="col-md-12"><div className="row">
            <div className="col-md-4 px-4"><img src="/assets/images/section_6.jpg" className="rounded-5" alt="Invest" /><div className="pt-4 text-center"><h3 className="text-dark">Personal Loans</h3><p className="text-dark">Handle life needs quickly and simply.</p></div></div>
            <div className="col-md-4 px-4"><img src="/assets/images/section_7.jpg" className="rounded-5" alt="Savings" /><div className="pt-4 text-center"><h3 className="text-dark">Business Loans</h3><p className="text-dark">Working capital, inventory, and expansion for SMEs.</p></div></div>
            <div className="col-md-4 px-4"><img src="/assets/images/section_8.jpg" className="rounded-5" alt="Loan" /><div className="pt-4 text-center"><h3 className="text-dark">Asset Financing</h3><p className="text-dark">Vehicles, equipment, and essential devices.</p></div></div>
          </div></div></div>
        </section>

        <section className="container mt-2 pt-3 pt-lg-5 pb-5">
          <div className="row align-items-lg-center pt-md-3 pb-5 mb-2 mb-lg-4 mb-xl-5">
            <div className="col-md-5 order-md-2 mb-4 mb-md-0"><img src="/assets/images/section_55.png" alt="Section" /></div>
            <div className="col-md-7 order-md-1">
              <div className="pe-xl-5 me-md-2 me-lg-4">
                <h2 className="display-4 pb-3 text-dark">Handle life needs quickly and simply.</h2>
                <p className="fs-3 text-start text-md-start pb-2 pb-md-3 mb-3 text-dark">You can now access quick loans in 5 mins with easy repayment terms!</p>
                <div className="d-md-flex align-items-md-start">
                  <Link href="/register" className="btn btn-info flex-shrink-0 me-md-4 mb-md-0 mb-sm-4 mb-3 rounded-pill">Apply Now</Link>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="container pt-4 pt-lg-0 pb-4 pb-lg-5">
          <div className="row align-items-lg-center pt-md-3 pb-5 mb-2 mb-lg-4 mb-xl-5">
            <div className="col-md-6 order-md-1 mb-4 mb-md-0 text-center"><img src="/assets/images/section_3.png" width="400" alt="Steps" /></div>
            <div className="col-md-6 order-md-2">
              <h2 className="h1 pb-3 pb-md-0 mb-md-5 text-dark">It only takes 5 minutes</h2>
              <div className="steps">
                <div className="step pt-0 pt-md-3 pb-5"><div className="step-number"><div className="step-number-inner text-info fs-md">01</div></div><div className="step-body d-flex align-items-center ps-xl-1"><div className="rellax ps-md-4 ps-xl-5" data-rellax-percentage="0.5" data-rellax-speed="0.4" data-disable-parallax-down="lg"><h3 className="h5 text-gray">Apply</h3><p className="mb-0">Tell us what you need and the amount.</p></div></div></div>
                <div className="step pt-0 pt-md-4 pb-5"><div className="step-number"><div className="step-number-inner text-info fs-md">02</div></div><div className="step-body d-flex align-items-center ps-xl-1"><div className="rellax ps-md-4 ps-xl-5" data-rellax-percentage="0.5" data-rellax-speed="0.5" data-disable-parallax-down="lg"><h3 className="h5 text-gray">Verify</h3><p className="mb-0">Share basic KYC where needed.</p></div></div></div>
                <div className="step pt-0 pt-md-4 pb-5"><div className="step-number"><div className="step-number-inner text-info fs-md">03</div></div><div className="step-body d-flex align-items-center ps-xl-1"><div className="rellax ps-md-4 ps-xl-5" data-rellax-percentage="0.5" data-rellax-speed="0.4" data-disable-parallax-down="lg"><h3 className="h5 text-gray">Offer</h3><p className="mb-0">Receive a clear offer with total cost shown upfront.</p></div></div></div>
                <div className="step pt-0 pt-md-4 pb-5"><div className="step-number"><div className="step-number-inner text-info fs-md">04</div></div><div className="step-body d-flex align-items-center ps-xl-1"><div className="rellax ps-md-4 ps-xl-5" data-rellax-percentage="0.5" data-rellax-speed="0.4" data-disable-parallax-down="lg"><h3 className="h5 text-gray">Disburse</h3><p className="mb-0">Funds go to you or the vendor.</p></div></div></div>
              </div>
            </div>
          </div>
        </section>

        <section className="container py-5 mb-2 mt-md-2 mb-md-4 mt-lg-4 mb-lg-5">
          <div className="row pt-xl-1 pb-xl-3 align-items-center justify-content-center">
            <div className="col-md-4"><h2 className="text-center text-md-start mx-auto mx-md-0 pt-md-2 fs-1 fw-semibold">Licensed and regulated, Yup!</h2><div className="d-flex justify-content-center justify-content-md-start pb-4 mb-2 pt-2 pt-md-4 mt-md-5"><button type="button" id="prev-testimonial" className="btn btn-prev btn-icon btn-md me-2"><i className="bx bx-chevron-left"></i></button><button type="button" id="next-testimonial" className="btn btn-next btn-icon btn-md ms-2"><i className="bx bx-chevron-right"></i></button></div></div>
            <div className="col-md-8"><div className="swiper mx-n2" data-swiper-options='{"slidesPerView":1,"spaceBetween":8,"autoplay":true,"loop":true,"navigation":{"prevEl":"#prev-testimonial","nextEl":"#next-testimonial"},"breakpoints":{"500":{"slidesPerView":2},"1000":{"slidesPerView":2},"1200":{"slidesPerView":2}}}'><div className="swiper-wrapper">
              <div className="swiper-slide h-auto pt-4"><figure className="d-flex flex-column px-2 px-sm-0 mb-0 mx-2"><div className="card position-relative border-0 shadow-sm pt-4 rounded-5 bg-gradient-primary"><figcaption className="d-flex align-items-center ps-4 pt-4"><img src="/assets/review/02k3PO8JVbKDlJnN7UGtSPPInm9qptoVeNsP0wLL.jpg" width="48" className="rounded-circle" alt="Jason Well" /><div className="ps-3"><h4 className="fs-5 fw-semibold mb-0">Jason Well</h4><span className="fs-sm text-dark">CEO Lorem Ipsum</span></div></figcaption><blockquote className="card-body pb-3 mb-5"><p className="mb-0 text-dark fs-4 fw-semibold">“Bajol Capital has been a lifesaver for me as a student in a foreign country”</p></blockquote></div></figure></div>
              <div className="swiper-slide h-auto pt-4"><figure className="d-flex flex-column px-2 px-sm-0 mb-0 mx-2"><div className="card position-relative border-0 shadow-sm pt-4 rounded-5 bg-gradient-primary"><figcaption className="d-flex align-items-center ps-4 pt-4"><img src="/assets/review/tiFOAsLHLYqTp2nEkiRqp7siYukGEBE3qESS1kHT.jpg" width="48" className="rounded-circle" alt="Cadi Jules" /><div className="ps-3"><h4 className="fs-5 fw-semibold mb-0">Cadi Jules</h4><span className="fs-sm text-dark">CEO Lorem Ipsum</span></div></figcaption><blockquote className="card-body pb-3 mb-5"><p className="mb-0 text-dark fs-4 fw-semibold">“Bajol Capital has been a lifesaver for me as a student in a foreign country”</p></blockquote></div></figure></div>
              <div className="swiper-slide h-auto pt-4"><figure className="d-flex flex-column px-2 px-sm-0 mb-0 mx-2"><div className="card position-relative border-0 shadow-sm pt-4 rounded-5 bg-gradient-primary"><figcaption className="d-flex align-items-center ps-4 pt-4"><img src="/assets/review/sF6AxGz1pCBh335dW5P4Tf11cM69m8Q3Yq3U6Dmx.jpg" width="48" className="rounded-circle" alt="JacK Mill" /><div className="ps-3"><h4 className="fs-5 fw-semibold mb-0">JacK Mill</h4><span className="fs-sm text-dark">CEO Lorem Ipsum</span></div></figcaption><blockquote className="card-body pb-3 mb-5"><p className="mb-0 text-dark fs-4 fw-semibold">“Bajol Capital has been a lifesaver for me as a student in a foreign country”</p></blockquote></div></figure></div>
            </div></div></div>
          </div>
        </section>

        <section className="container pt-3 pb-5 pb-md-5"><div className="card border-0"><div className="card-body p-md-5 p-4 bg-size-cover rounded-5" style={{ backgroundImage: "url(/assets/images/live.png)" }}><div className="py-md-5 py-4 text-md-start"><p className="display-6 text-white mb-1">What are you waiting for?</p><p className="fs-5 text-white">Get financing today.</p><div className="pt-md-5 pt-4 pb-md-2"><Link href="/dashboard" className="btn btn-lg btn-light mx-2 rounded-pill">Apply Now</Link></div></div></div></div></section>

        <section className="container mt-2 pt-3 pt-lg-5 pb-5">
          <h2 className="h3 text-center pb-3 pb-md-0 text-gray">Our Partners</h2>
          <div className="swiper mx-n2" data-swiper-options='{"slidesPerView":2,"pagination":{"el":".swiper-pagination","clickable":true},"breakpoints":{"500":{"slidesPerView":3,"spaceBetween":8},"650":{"slidesPerView":4,"spaceBetween":8},"900":{"slidesPerView":5,"spaceBetween":8},"1100":{"slidesPerView":6,"spaceBetween":8}}}'>
            <div className="swiper-wrapper">
              <div className="swiper-slide py-3"><div className="card card-body card-hover px-2 mx-2"><img src="/assets/brand/JMrzjE3SZN1jxLoKVFKZicq58NqvILJRNJF7lEx9.svg" className="d-block mx-auto my-2" width="150" alt="Brand" /></div></div>
              <div className="swiper-slide py-3"><div className="card card-body card-hover px-2 mx-2"><img src="/assets/brand/jLUaA21JPmjs3KUj0BCVnpL6BBV30fnsD8vfc1w9.svg" className="d-block mx-auto my-2" width="150" alt="Brand" /></div></div>
              <div className="swiper-slide py-3"><div className="card card-body card-hover px-2 mx-2"><img src="/assets/brand/8g1m0KJ76WU58gyyqOAy4YYvLn2eZKSqM3ZdnA1w.svg" className="d-block mx-auto my-2" width="150" alt="Brand" /></div></div>
              <div className="swiper-slide py-3"><div className="card card-body card-hover px-2 mx-2"><img src="/assets/brand/OVSD1zu2K77urzbdoYAy8ozVhtzPi9YIUX0Fe8dc.svg" className="d-block mx-auto my-2" width="150" alt="Brand" /></div></div>
              <div className="swiper-slide py-3"><div className="card card-body card-hover px-2 mx-2"><img src="/assets/brand/IzqjdGAO4EGJKYWiDKGAqfN9DRevcgUPZebKv7n6.svg" className="d-block mx-auto my-2" width="150" alt="Brand" /></div></div>
              <div className="swiper-slide py-3"><div className="card card-body card-hover px-2 mx-2"><img src="/assets/brand/SEZ8wiBnYhSVG1Kmifjs0jx0cGXcp1kMi9FqSV4l.svg" className="d-block mx-auto my-2" width="150" alt="Brand" /></div></div>
              <div className="swiper-slide py-3"><div className="card card-body card-hover px-2 mx-2"><img src="/assets/brand/v6g8eNolrPIwwV4aNIOfTCuaHF1GBzBkNMyZaafp.svg" className="d-block mx-auto my-2" width="150" alt="Brand" /></div></div>
            </div>
            <div className="swiper-pagination position-relative pt-2 mt-4"></div>
          </div>
        </section>

        <PublicSiteFooter />
      </main>
      <PublicSiteScripts />
    </>
  );
}
