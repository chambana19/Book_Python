% Auth: Nicklas Vraa
% Docs: https://github.com/NicklasVraa/LiX
% ------------------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{textbook}[2025/09/01 For academic textbooks]

% Intercept class options.
\newcommand{\numColumns}{1}
\DeclareOption{twocolumn}{
    \renewcommand{\numColumns}{2}
    \PassOptionsToClass{\CurrentOption}{report}
}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass{report}

% SETUP: -----------------------------------------------------------------------
\RequirePackage[basics, code, cover, figures, formatting, header, headings, isbn, license, lists, math, metadata, publish, refs, size, tables]{lix}
\RequirePackage{parskip, setspace, silence, titlesec, titletoc, titling}
\RequirePackage{lastpage} % <<< add: provides \pageref{LastPage}

\WarningsOff*
\setlength\parindent{0pt}

% SIZE, MARGINS: ---------------------------------------------------------------
\geometry{letterpaper, top=30mm, bottom=30mm, left=24mm, right=24mm}
\setlength{\columnsep}{5mm}

% COVER: -----------------------------------------------------------------------
\setlength{\droptitle}{-110mm}%

% TABLE OF CONTENTS: -----------------------------------------------------------
\titlecontents{section}[0em]{}{%
    \thecontentslabel.\hspace*{1em}}{}{%
    \titlerule*[0.5pc]{.}\contentspage%
}
\titlecontents{subsection}[0em]{%
    \hspace*{2em}}{\thecontentslabel.\hspace*{0.5em}}{}{%
    \titlerule*[0.5pc]{.}\contentspage%
}
\titlecontents{subsubsection}[0em]{%
    \hspace*{4em}}{\thecontentslabel.\hspace*{0.5em}}{}{%
    \titlerule*[0.5pc]{.}\contentspage%
}

% HEADER AND FOOTER: -----------------------------------------------------------
\setlength{\headsep}{5mm}%
\pagestyle{fancy}%
\renewcommand{\headrulewidth}{0pt}%
\renewcommand{\footrulewidth}{0.4pt}%
\renewcommand{\chaptermark}[1]{\markboth{#1}{#1}}%
\fancyhead[L]{%
    \small\scshape\color{darkgray} \chaptername\ \thechapter%
}
\fancyhead[R]{%
    % The page counter now lives in the footer, which is what previously
    % collided with a long chapter title here. A smaller size gives even the
    % longest chapter titles (e.g. Chapter 20) room against the left tag.
    \footnotesize\scshape\color{darkgray} \leftmark%
}
\fancyfoot[L]{%
    \footnotesize\color{darkgray}\hyperref[book:toc]{Contents}%
}
\fancyfoot[R]{%
    \footnotesize\color{darkgray} Page \thepage\ of \pageref{LastPage}% <<< keep \pageref
}

% HEADINGS: --------------------------------------------------------------------
\setcounter{secnumdepth}{4}% Levels of heading that will be numbered.
\renewcommand*{\@seccntformat}[1]{% Add dot after number.
    \csname the#1\endcsname.\hspace{0.5em}%
}
\titlespacing{\chapter}{-1pt}{-45pt}{4pt}
\titlespacing\numberless{0pt}{14pt}{4pt}
\titlespacing\section{0pt}{14pt}{4pt}
\titlespacing\subsection{0pt}{14pt}{4pt}
\titlespacing\subsubsection{0pt}{14pt}{4pt}
\titleformat*{\section}{\bfseries\scshape}
\titleformat*{\subsection}{\bfseries\scshape}
\titleformat*{\subsubsection}{\bfseries\scshape}
\titleformat*{\paragraph}{\bfseries\scshape}
\titleformat{\chapter}[display]{%
    \normalsize%
}{% Prefix.
    % The page counter lives in the footer on every other page; this opening
    % page uses \thispagestyle{empty} below, so it stays deliberately quiet.
    \hspace{1pt}\small\scshape\color{darkgray}\chaptertitlename \ \thechapter%
}{% Vertical space between.
    \ifnum\numColumns=1%
        4pt%
    \else
        2pt%
    \fi
}{% Chapter name.
    \thispagestyle{empty}\LARGE\bfseries\scshape%
}

% CAPTIONS: --------------------------------------------------------------------
\captionsetup{
    format=plain, labelfont=bf, font=scriptsize,
    justification=raggedright, singlelinecheck=false
}

% LAYOUT: ----------------------------------------------------------------------
\wrap{%
    % This section defines how \title, \author, etc. will behave if used,
    % but does not output anything on its own. It's safe to keep.
    \@ifundefined{theTitle}{}{%
        \@ifundefined{theSubtitle}{%
            \oldtitle{\Huge\textbf{\textsc{\theTitle}}}%
        }{%
            \oldtitle{\Huge\textbf{\textsc{\theTitle}}\\[0.4ex]%
            \large\scshape\theSubtitle}%
        }
    }
    \@ifundefined{theAuthor}{%
        \oldauthor{}%
    }{%
        \oldauthor{\normalsize{\theAuthor}}%
    }
    \@ifundefined{theDate}{%
        \olddate{}%
    }{%
        \olddate{\normalsize{\theDate}}%
    }
    % This command is also safe as it only adds data to the PDF metadata.
    \addMetadata

    % --- The problematic commands have been removed ---
    % \addFrontCover
    % \addBackCover
    % \ifnum\printOnCover=1 ... \fi
    % \addFormalPage
}

% Ensure LastPage label is written on the actual final page:
\AtEndDocument{\label{LastPage}} % <<< add
