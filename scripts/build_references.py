#!/usr/bin/env python3
"""Rebuild REFERENCES.md and renumber every citation marker consistently.

Maps each legacy marker number to a source key, assigns new numbers in order of
first appearance across the chapters, rewrites the chapter files and the source_ref
columns in data/*.csv, then writes REFERENCES.md.
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# key -> (title, url)
SOURCES = {
 "GP_WIKI": ("Great Pyramid of Giza. Wikipedia.", "https://en.wikipedia.org/wiki/Great_Pyramid_of_Giza"),
 "WIKI_CONSTRUCTION": ("Construction of the Egyptian pyramids. Wikipedia.", "https://en.wikipedia.org/wiki/Construction_of_the_Egyptian_pyramids"),
 "WIKI_QUARRIES": ("Stone quarries of ancient Egypt. Wikipedia.", "https://en.wikipedia.org/wiki/Stone_quarries_of_ancient_Egypt"),
 "WIKI_MERER": ("Diary of Merer. Wikipedia.", "https://en.wikipedia.org/wiki/Diary_of_Merer"),
 "WIKI_SCANPYRAMIDS": ("ScanPyramids. Wikipedia.", "https://en.wikipedia.org/wiki/ScanPyramids"),
 "WIKI_HOUDIN": ("Jean-Pierre Houdin. Wikipedia.", "https://en.wikipedia.org/wiki/Jean-Pierre_Houdin"),
 "WIKI_DAVIDOVITS": ("Joseph Davidovits. Wikipedia.", "https://en.wikipedia.org/wiki/Joseph_Davidovits"),
 "WIKI_DJOSER": ("Pyramid of Djoser. Wikipedia.", "https://en.wikipedia.org/wiki/Pyramid_of_Djoser"),
 "WH_STEPPYRAMID": ("The Step Pyramid of Djoser at Saqqara. World History Encyclopedia.", "https://www.worldhistory.org/article/862/the-step-pyramid-of-djoser-at-saqqara/"),
 "WH_IMHOTEP": ("Imhotep. World History Encyclopedia.", "https://www.worldhistory.org/imhotep/"),
 "COPAS": ("Copas, M. (2026). Systemic Capacity Constraints in the Khufu Programme (Construction). Zenodo.", "https://zenodo.org/records/20001495/files/Copas_M_2026a_Systemic%20Constraints%20in%20the%20Khufu%20Programme%20Construction.pdf?download=1"),
 "HS_MORTAR": ("Sustainability problems of the Giza pyramids. npj Heritage Science (2020).", "https://www.nature.com/articles/s40494-020-0356-9"),
 "HS_SAHURE": ("Geoenvironmental investigation of Sahure's pyramid, Abusir. npj Heritage Science (2022).", "https://www.nature.com/articles/s40494-022-00699-1"),
 "ZEN_COMPOSITE": ("Between Precision and Pragmatism: A Composite Material Model for Pyramid Construction. Zenodo (2026).", "https://zenodo.org/records/18990874"),
 "PREPRINT_RAMP": ("Mastabas, Back-and-Forth Ramps and Finishing from the Top. Preprints.org (2026).", "https://www.preprints.org/manuscript/202610.0852"),
 "CSMONITOR": ("Ancient Egyptians used wet sand to drag massive pyramid stones, say scientists. The Christian Science Monitor (2014).", "https://www.csmonitor.com/Science/2014/0502/Ancient-Egyptians-used-wet-sand-to-drag-massive-pyramid-stones-say-scientists"),
 "RIGBY": ("Rigby, M. (2016). Building The Great Pyramid At Giza: Investigating Ramp Models.", "https://archaeology.brown.edu/sites/default/files/papers/Rigby2016.pdf"),
 "BLOXAM_UCL": ("Bloxam, E. Who were the pharaohs' quarrymen? Archaeology International, UCL Press.", "https://journals.uclpress.co.uk/ai/article/795/galley/13225/view/"),
 "BLOXAM_OVERVIEW": ("Bloxam, E. & Harrell, J. Ancient Egyptian quarries: an illustrated overview.", "https://www.academia.edu/1360554/Ancient_Egyptian_quarries_an_illustrated_overview_co_authored_with_James_Harrell_"),
 "TAYLOR_MORTAR": ("Mortar and Concrete: Precursors to Modern Materials. International Journal of Masonry (2023).", "https://www.tandfonline.com/doi/full/10.1080/15583058.2023.2235319"),
 "HISTORYTODAY": ("Monumental Record. History Today.", "http://www.historytoday.com/archive/history-matters/monumental-record"),
 "SIS": ("Parts of papyrus archive of King Khufu displayed at Tahrir's Egyptian Museum. State Information Service, Egypt.", "https://www.sis.gov.eg/Story/103148"),
 "ARXIV_TIME": ("Timekeeping at Akhet Khufu, as shown by the Diary of Merer. arXiv:2411.08061.", "https://arxiv.org/pdf/2411.08061"),
 "CEE_AHRAMAT": ("Ghoneim, E., Ralph, T.J., et al. (2024). The Egyptian pyramid chain was built along the now abandoned Ahramat Nile Branch. Communications Earth & Environment 5, 233.", "https://www.nature.com/articles/s43247-024-01379-7"),
 "AERAGRAM": ("AERAgram Volume 14, No. 1. Ancient Egypt Research Associates.", "https://www.academia.edu/8714264/AERAgram_Volume_14_No_1"),
 "AERA_LOSTCITY": ("The Lost City of the Pyramids (Heit el-Ghurab). Ancient Egypt Research Associates.", "https://aeraweb.org/projects/lost-city//"),
 "ARCH_PORT": ("Port of the Pyramids. Archaeology Magazine (2014).", "https://archaeology.org/issues/may-june-2014/digs-discoveries/egypt-giza-wealthy-nile-port/"),
 "CDLIB": ("Quarrying and Mining (Stone). University of California.", "https://repositories.cdlib.org/content/qt9bb918sd/qt9bb918sd.pdf"),
 "MEDOMED": ("Gebel Qatrani and the ancient quarries of Widan el-Faras and Umm es-Sawan. Medomed.", "https://medomed.org/featured_item/gebel-qatrani-and-the-ancient-quarries-of-widan-el-faras-and-umm-es-sawan-in-fayoum-depression-egypt/"),
 "OBELISKS": ("Chapter 3: transport of stone. Obelisks.org.", "https://www.obelisks.org/pyramids/chapter-3.pdf"),
 "OBSERVATORY": ("The Great Ascent: Solving the Pyramid's Ramp Riddle. Observatory Wiki.", "https://observatory.wiki/The_Great_Ascent:_Solving_the_Pyramid's_Ramp_Riddle/info"),
 "PRL": ("Fall, A., Weber, B., Pakpour, M., et al. (2014). Sliding friction on wet and dry sand. Physical Review Letters 112, 175502.", "https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.112.175502"),
 "THEORIES": ("Construction Replication Experiments: Testing Ancient Building Claims. Theories of Anything.", "https://theoriesofanything.com/research/construction-replication-experiments-testing-ancient-building-claims"),
 "MAPPING_IGN": ("Moving pyramid stones on sand. Mapping Ignorance (2014).", "https://mappingignorance.org/2014/07/18/moving-pyramid-stones-sand/"),
 "UVA_BACK": ("Bonn, D. Sliding Friction on Wet and Dry Sand (doctoral thesis, back matter). University of Amsterdam.", "https://pure.uva.nl/ws/files/60615185/Back_matter.pdf"),
 "BREWMINATE": ("Pyramid Construction Techniques in Ancient Egypt. Brewminate.", "https://brewminate.com/pyramid-construction-techniques-in-ancient-egypt/"),
 "ARXIV_WEST": ("West, J. et al. How they (should have) built the pyramids. arXiv:1408.3603.", "https://arxiv.org/pdf/1408.3603v1"),
 "GIZMODO": ("Physicists Have A Simple Answer For How Egyptians Built The Pyramids. Gizmodo.", "https://gizmodo.com/physicists-have-a-simple-answer-for-how-egyptians-built-1627604283"),
 "UPENN": ("Moving and Lifting the Construction Blocks of the Great Pyramid. University of Pennsylvania.", "https://www.ling.upenn.edu/~jason2/papers/pyramid.htm"),
 "IEEE": ("How Many People Did it Take to Build the Great Pyramid? IEEE Spectrum.", "https://spectrum.ieee.org/how-many-people-did-it-take-to-build-the-great-pyramid"),
 "NOVA_BUILDERS": ("Who Built the Pyramids? Builders. NOVA / PBS.", "https://www.pbs.org/wgbh/nova/pyramid/explore/builders.html"),
 "BBC_PRIVATES": ("The Private Lives of the Pyramid-builders. BBC History.", "https://www.bbc.com/history/ancient/egyptians/pyramid_builders_01.shtml"),
 "DIGITALGIZA": ("Who built the pyramids? Paid Egyptian crews, not slaves. Digital Giza / Our Earth History.", "https://ourearthshistory.com/africa/ancient/who-built-the-pyramids/"),
 "THEARTNEWBIE": ("How Were the Pyramids Built? What the Evidence Shows. The Art Newbie.", "https://theartnewbie.com/art-history/ancient-egypt/how-the-pyramids-were-built/"),
 "SMITHSONIAN": ("Monumental Shift. Smithsonian Magazine.", "https://www.smithsonianmag.com/science-nature/monumental-shift-160227897/"),
 "HS_EDGE": ("A computational framework for evaluating an edge-integrated, multi-ramp construction model of the Great Pyramid of Giza. npj Heritage Science (2026).", "https://www.nature.com/articles/s40494-026-02405-x"),
 "K_DENSE": ("Engineering Analysis of Great Pyramid Construction Models. K-Dense.", "https://www.k-dense.ai/examples/session_20251224_105449_4bd8fa278c83/writing_outputs/final/pyramid_engineering_analysis.pdf"),
 "NBC_HOUDIN": ("Was Great Pyramid built from inside out? NBC News.", "https://www.nbcnews.com/id/wbna17873984"),
 "BBC_HOUDIN": ("Mystery of Great Pyramid 'solved'. BBC News.", "http://news.bbc.co.uk/2/hi/middle_east/6514155.stm"),
 "HS_PULLEY": ("Construction of the Great Pyramid with pulley-like systems fueled by sliding counterweights. npj Heritage Science (2025).", "https://www.nature.com/articles/s40494-025-02018-w"),
 "ANCIENTEGYPTONLINE": ("Great Pyramid: King's Chamber. Ancient Egypt Online.", "https://ancientegyptonline.co.uk/kingschambergp/"),
 "ARTNEWBIE_INSIDE": ("Inside the Pyramids of Giza: What Is Really in There? The Art Newbie.", "https://theartnewbie.com/art-history/ancient-egypt/inside-pyramid-giza/"),
 "KHUFUPYRAMID": ("The King's Chamber - The Khufu Pyramid.", "https://khufupyramid.dk/inside-dimensions/the-kings-chamber"),
 "FACTCHECK": ("Fact check: Graham Hancock on Archaeology, JRE #1284.", "https://www.factcheckjoerogan.com/claims/cmrezlfqp000t4z6hsn8q55m4"),
 "TUM": ("ScanPyramids Project. Technical University of Munich.", "https://www.mae.ed.tum.de/en/zfp/forschungsprojekte/scanpyramids-project/"),
 "BBC_BUILDING": ("Building The Great Pyramid. BBC History.", "https://www.bbc.co.uk/history/ancient/egyptians/great_pyramid_01.shtml"),
 "MIATELLO": ("Miatello, M. (2010). The Grand Gallery and the King's Chamber of the Great Pyramid of Khufu. PalArch's Journal of Archaeology of Egypt/Egyptology 7(6).", "http://gizamedia.rc.fas.harvard.edu/documents/miatello_pjaee_7-6_2010.pdf"),
 "SCI_REP_SEISMIC": ("Architectural and geotechnical aspects affecting earthquake resilience for the antique Egyptian Khufu pyramid. Scientific Reports (2026).", "https://www.nature.com/articles/s41598-026-49962-6"),
 "NATGEO": ("How ancient builders made the Great Pyramid of Giza nearly earthquake-proof. National Geographic.", "https://www.nationalgeographic.com/history/article/giza-pyramid-earthquake"),
 "SCIENCEALERT": ("The Great Pyramid Has Survived 4,600 Years. A Strange Feature May Help Explain Why. ScienceAlert.", "https://www.sciencealert.com/the-great-pyramid-has-survived-4600-years-a-strange-feature-may-help-explain-why"),
 "DASH_PAULSON": ("Dash, G. & Paulson, J. (2016). The 2015 Survey of the Base of the Great Pyramid. Journal of Egyptian Archaeology.", "https://www.academia.edu/36742756/The_2015_Survey_of_the_Base_of_the_Great_Pyramid"),
 "DASH_ASPUB": ("Archaeology - As Published. Glen Dash.", "https://www.glendash.com/archaeology/as-published.html"),
 "LIGHTBODY": ("Lightbody, G. Moving heaven and earth for Khufu: Were the Trial Passages at Giza for astronomical observation? Journal of Ancient Egyptian Architecture 4.", "https://web.ujaen.es/investiga/egiptologia/journalarchitecture/downloads/JAEA4/JAEA4_Lightbody.pdf"),
 "DASH_OCCAM": ("Dash, G. The simplest explanation may reveal the odd alignment of Egypt's Great Pyramids (Occam's razor paper).", "https://mqtrinh.github.io/other/egyptian/dash_occam-s-egyptian-razor.pdf"),
 "DASH_FIELD": ("Dash, G. (2015). On the Field Testing of Methods the Egyptians May Have Used to Find Cardinal Directions. Journal of Egyptian Archaeology.", "https://journals.sagepub.com/doi/10.1177/0021828615593272"),
 "SCIENCEALERT_ALIGN": ("The Secret of The Pyramids' Perfect Alignment Might Be Explained After All. ScienceAlert.", "https://www.sciencealert.com/the-secret-of-the-pyramids-perfect-alignment-might-be-explained-after-all"),
 "NOVA_ARTICLE": ("Who Built the Pyramids? NOVA / PBS.", "https://www.pbs.org/wgbh/nova/article/who-built-the-pyramids/"),
 "HARVARDMAG": ("Who Built the Pyramids? Harvard Magazine (2003).", "https://www.harvardmagazine.com/2003/07/who-built-the-pyramids-html"),
 "LIVESCOPE_WORKERS": ("Giza Secret Revealed: How 10,000 Pyramid Builders Got Fed. Live Science.", "https://www.livescience.com/28961-ancient-giza-pyramid-builders-camp-unearthed.html"),
 "AERA_2023": ("AERA Annual Report 2023. Ancient Egypt Research Associates.", "https://aeraweb.org/wp-content/uploads/2025/03/AERA_2023.pdf"),
 "AERA_2014": ("AERA Annual Report 2014. Ancient Egypt Research Associates.", "https://aeraweb.org/wp-content/uploads/2022/08/AERA_2014.pdf"),
 "AERA_AR2017": ("Annual Report 2017. Ancient Egypt Research Associates.", "https://www.aeraweb.org/wp-content/uploads/2019/05/AR2017.pdf"),
 "NATURE2017": ("Morishima, K., Kuno, M., et al. (2017). Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons. Nature 552, 386-390.", "https://www.nature.com/articles/nature24647"),
 "PUBMED2017": ("Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons. PubMed (PMID 29160306).", "https://pubmed.ncbi.nlm.nih.gov/29160306/"),
 "ARXIV2017": ("Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons. arXiv:1711.01576.", "https://ar5iv.arxiv.org/html/1711.01576"),
 "PHYSORG_HAWASS": ("Egypt archaeologist criticises pyramid void 'discovery'. Phys.org (2017).", "https://phys.org/news/2017-11-egypt-archaeologist-criticises-pyramid-void.html"),
 "NATCOMMS2023": ("Procureur, S., Morishima, K., Kuno, M., et al. (2023). Precise characterization of a corridor-shaped structure in Khufu's Pyramid by observation of cosmic-ray muons. Nature Communications 14, 1144.", "https://www.nature.com/articles/s41467-023-36351-0"),
 "NDT2023": ("Elkarmoty, M., Rupfle, J., et al. (2023). Localization and shape determination of a hidden corridor in the Great Pyramid of Giza using non-destructive testing. NDT & E International.", "https://doi.org/10.1016/j.ndteint.2023.102809"),
 "ARCHWIKI_2023": ("Unknown room discovered in the Great Pyramid. Archaeology Wiki (2023).", "https://www.archaeology.wiki/blog/2023/03/03/unknown-room-discovered-in-the-great-pyramid/"),
 "INVERSE": ("Cosmic Rays Reveal A Hidden Corridor in the Great Pyramid of Giza. Inverse.", "https://www.inverse.com/science/cosmic-rays-great-pyramid"),
 "SCIREP_FUSION": ("Schumacher, T., Pugacheva, P., et al. (2025). Confirmation of the ScanPyramids North Face Corridor in the Great Pyramid of Giza using multi-modal image fusion from three non-destructive testing techniques. Scientific Reports 15, 9275.", "https://www.nature.com/articles/s41598-025-91115-8"),
 "SCIREP_ERT": ("Pugacheva, P., Allam, H., et al. (2025). Investigation of the North Face Corridor in the Great Pyramid of Giza using Electrical Resistivity Tomography. Scientific Reports 15, 41187.", "https://www.nature.com/articles/s41598-025-29081-4"),
 "ARCH_MENKAURE": ("Scientists Scan Egypt's Menkaure Pyramid with High-Tech Tools. Archaeology Magazine (2025).", "https://archaeology.org/news/2025/11/13/scientists-scan-egypts-menkaure-pyramid-with-high-tech-tools/"),
 "AHRAM_RETRACTION": ("Great Pyramid radar study on 'hidden structures' retracted. Ahram Online (2026).", "https://english.ahram.org.eg/NewsContent/1/1238/576187/Egypt/Tourism/Great-Pyramid-radar-study-on;hidden-structures;-r.aspx"),
 "TIMESOFINDIA": ("A robot traveled to Great Pyramid via hidden path and stopped in front of a door that had remained sealed for 4,500 years. Times of India (2026).", "https://timesofindia.indiatimes.com/technology/tech-news/a-robot-traveled-to-great-pyramid-via-hidden-path-and-stopped-in-front-of-a-door-that-had-remained-sealed-for-4500-years-heres-what-happened/articleshow/133221874.cms"),
 "ARKEONEWS": ("Great Pyramid Radar Study Retracted, but the Pyramid's Hidden Voids Haven't Gone Away. Arkeonews (2026).", "https://arkeonews.net/great-pyramid-radar-study-retracted-but-the-pyramids-hidden-voids-havent-gone-away/"),
 "RETRACTION_WATCH": ("Journal retracts paper claiming network of corridors inside the Great Pyramid of Giza. Retraction Watch (2026).", "https://retractionwatch.com/category/by-journal/page/2/"),
 "ANCIENTSKY": ("Beneath Giza: What Is Confirmed and What Is Only Claimed About Hidden Structures. The Ancient Sky.", "https://theancientsky.com/the-weird/pyramids-hidden-structures/"),
 "JPOST": ("Zahi Hawass teases 2026 Great Pyramid reveal. The Jerusalem Post (2025).", "https://www.jpost.com/archaeology/article-873314"),
 "EGYPTINDEP": ("Egypt to announce archaeological surprise in 2026 that will 'rewrite history'. Egypt Independent (2025).", "https://www.egyptindependent.com/egypt-to-announce-archaeological-surprise-in-2026-that-will-rewrite-history-zahi-hawass/"),
 "DUNN_BOOK": ("Dunn, C. (1998). The Giza Power Plant: Technologies of Ancient Egypt.", "https://library.tacaids.go.tz/papersCollection/virtual-library/index_htm_files/the_giza_power_plant_technologies_of_ancient_egypt_christopher_dunn.pdf"),
 "GEOPOLYMER": ("Are Pyramids Made Out of Concrete? (1). Geopolymer Institute.", "https://www.geopolymer.org/archaeology/pyramids/are-pyramids-made-out-of-concrete-1/"),
 "CEN1984": ("Pyramids are not made of polymers, say experts. Chemical & Engineering News (1984).", "https://pubs.acs.org/doi/abs/10.1021/cen-v062n021.p005"),
 "CENVILLE": ("Pyramids in Concrete. University of Memphis.", "http://www.ce.memphis.edu/1101/interesting_stuff/pyramids_in_concrete.html"),
 "WIKQUOTE_JANA": ("Joseph Davidovits (quoting D. Jana, 'The Great Pyramid Debate'). Wikiquote.", "https://en.wikiquote.org/wiki/Joseph_Davidovits"),
 "DLAB_EPFL": ("Great Pyramid of Giza (schematic data incl. Grand Gallery sockets and floor trench). EPFL DLAB mirror of the 1911 Britannica entry.", "https://dlab.epfl.ch/wikispeedia/wpcd/wp/g/Great_Pyramid_of_Giza.htm"),
 "PETROGRAPHIC": ("Petrographic Observations of the Building Stones of the Great Pyramid of Giza.", "https://pdfs.semanticscholar.org/437f/7920ba05527cad477df7512bc17bba684181.pdf"),
}

# legacy marker number -> source key
OLD_TO_KEY = {
 1:"GP_WIKI", 8:"WIKI_DJOSER", 12:"KHUFUPYRAMID", 13:"DLAB_EPFL", 14:"WH_STEPPYRAMID", 15:"WH_IMHOTEP", 16:"COPAS",
 17:"WIKI_SCANPYRAMIDS", 18:"HS_MORTAR", 19:"HS_SAHURE", 20:"ZEN_COMPOSITE",
 21:"PREPRINT_RAMP", 22:"WIKI_QUARRIES", 23:"CSMONITOR", 24:"RIGBY", 25:"BLOXAM_UCL",
 26:"BLOXAM_OVERVIEW", 27:"TAYLOR_MORTAR", 28:"WIKI_DAVIDOVITS", 29:"HISTORYTODAY",
 30:"WIKI_MERER", 31:"SIS", 32:"ARXIV_TIME", 33:"CEE_AHRAMAT", 34:"AERAGRAM",
 35:"AERA_LOSTCITY", 36:"ARCH_PORT", 37:"CDLIB", 38:"MEDOMED", 39:"OBELISKS",
 40:"BLOXAM_OVERVIEW", 41:"OBSERVATORY", 42:"PRL", 43:"THEORIES", 44:"MAPPING_IGN",
 45:"UVA_BACK", 46:"BREWMINATE", 47:"ARXIV_WEST", 48:"GIZMODO", 49:"GIZMODO",
 50:"UPENN", 51:"UPENN", 52:"UPENN", 53:"UPENN", 54:"IEEE", 55:"NOVA_BUILDERS",
 56:"BBC_PRIVATES", 57:"DIGITALGIZA", 58:"NOVA_BUILDERS", 59:"THEARTNEWBIE",
 61:"WIKI_CONSTRUCTION", 62:"SMITHSONIAN", 63:"HS_EDGE", 64:"WIKI_HOUDIN",
 65:"K_DENSE", 66:"NBC_HOUDIN", 67:"BBC_HOUDIN", 68:"HS_PULLEY",
 69:"SCI_REP_SEISMIC", 70:"ANCIENTEGYPTONLINE", 71:"ARTNEWBIE_INSIDE",
 72:"KHUFUPYRAMID", 73:"FACTCHECK", 74:"TUM", 75:"BBC_BUILDING", 76:"MIATELLO",
 77:"ARTNEWBIE_INSIDE", 78:"SCI_REP_SEISMIC", 79:"NATGEO", 80:"SCIENCEALERT",
 81:"GP_WIKI", 82:"DASH_PAULSON", 83:"DASH_ASPUB", 84:"LIGHTBODY", 85:"DASH_OCCAM",
 86:"DASH_FIELD", 87:"SCIENCEALERT_ALIGN", 88:"LIGHTBODY", 89:"NOVA_ARTICLE",
 90:"HARVARDMAG", 91:"BBC_PRIVATES", 92:"IEEE", 93:"BBC_PRIVATES", 94:"HARVARDMAG",
 95:"AERA_2023", 96:"LIVESCOPE_WORKERS", 97:"AERA_2014", 98:"AERA_2023",
 99:"NATURE2017", 100:"PUBMED2017", 101:"ARXIV2017", 102:"WIKI_SCANPYRAMIDS",
 103:"PHYSORG_HAWASS", 104:"NATCOMMS2023", 105:"NDT2023", 106:"ARCHWIKI_2023",
 107:"INVERSE", 108:"SCIREP_FUSION", 109:"SCIREP_ERT", 110:"TUM", 111:"ARCH_MENKAURE",
 112:"AHRAM_RETRACTION", 113:"TIMESOFINDIA", 114:"ARKEONEWS", 115:"JPOST",
 116:"EGYPTINDEP", 117:"DUNN_BOOK", 118:"GEOPOLYMER", 119:"CEN1984", 120:"CENVILLE",
 121:"WIKQUOTE_JANA", 122:"PETROGRAPHIC", 123:"RETRACTION_WATCH", 124:"ANCIENTSKY",
}

CITATION_RE = re.compile(r"\[(\d+)\](?!\()")


def chapter_files():
    files = sorted(f for f in os.listdir(ROOT)
                   if f.endswith(".md") and f != "REFERENCES.md")
    def key(f):
        m = re.match(r"^(\d+)-", f)
        return (0, int(m.group(1))) if m else (1, f)
    return sorted(files, key=key)


def main():
    order = []
    seen = set()
    for fname in chapter_files():
        text = open(os.path.join(ROOT, fname), encoding="utf-8").read()
        for m in CITATION_RE.finditer(text):
            old = int(m.group(1))
            if old not in OLD_TO_KEY:
                sys.exit(f"unmapped marker [{old}] in {fname}")
            key = OLD_TO_KEY[old]
            if key not in seen:
                seen.add(key)
                order.append(key)

    new_number = {k: i + 1 for i, k in enumerate(order)}
    old_to_new = {old: new_number[k] for old, k in OLD_TO_KEY.items()}

    # Rewrite chapter files
    for fname in chapter_files():
        path = os.path.join(ROOT, fname)
        text = open(path, encoding="utf-8").read()
        new = CITATION_RE.sub(lambda m: f"[{old_to_new[int(m.group(1))]}]", text)
        if new != text:
            open(path, "w", encoding="utf-8").write(new)

    # Rewrite source_ref columns in data CSVs
    for csv_name in ("pyramid_facts.csv", "alignment.csv"):
        path = os.path.join(ROOT, "data", csv_name)
        with open(path, newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        if not rows:
            continue
        header = rows[0]
        if "source_ref" not in header:
            continue
        col = header.index("source_ref")
        for row in rows[1:]:
            if col < len(row):
                raw = row[col].strip()
                if raw.isdigit():
                    row[col] = str(old_to_new[int(raw)])
        with open(path, "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(rows)

    # Write REFERENCES.md
    lines = ["# References", "",
             "Every citation marker used in the chapters resolves to exactly one entry below. "
             "Entries are ordered by first appearance. Where a source was consulted through a "
             "secondary report, that is stated in the entry.", "",
             "---", ""]
    for i, key in enumerate(order, start=1):
        title, url = SOURCES[key]
        lines.append(f"[{i}]. {title}")
        lines.append(f"    {url}")
        lines.append("")
    open(os.path.join(ROOT, "REFERENCES.md"), "w", encoding="utf-8").write("\n".join(lines))

    print(f"Renumbered {len(order)} sources across {len(chapter_files())} files.")
    print(f"New numbering: 1-{len(order)}")


if __name__ == "__main__":
    main()
