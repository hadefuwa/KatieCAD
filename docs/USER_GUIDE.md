# KatieCAD – Quick Guide (English)

> Deutsche Version: [ANLEITUNG.md](ANLEITUNG.md)

KatieCAD is a 2D CAD program with an electrical-engineering extension. This guide
shows where to find the basic functions. It is meant as a refresher if you have not
used the program for a while, or if you see it for the first time.

## Contents

1. [Starting](#1-starting)
2. [The window at a glance](#2-the-window-at-a-glance)
3. [Navigating, snapping, command line](#3-navigating-snapping-command-line)
4. [Drawing and editing](#4-drawing-and-editing)
5. [Projects and sheets](#5-projects-and-sheets)
6. [Model, layout, frame, printing](#6-model-layout-frame-printing)
7. [Blocks and attributes](#7-blocks-and-attributes)
8. [Electrical: drawing a schematic](#8-electrical-drawing-a-schematic)
9. [Generating documentation](#9-generating-documentation)
10. [Import and export](#10-import-and-export)
11. [Keyboard shortcuts](#11-keyboard-shortcuts)
12. [Tips and frequently asked questions](#12-tips-and-frequently-asked-questions)

---

## 1. Starting

```
python main.py
```

or `python -m katiecad`. Optionally install the extra packages with
`pip install -r requirements.txt` (needed for DXF/DWG import and DXF export). On Linux
you also need `python3-tk`.

Change the language in the **Language** menu (Deutsch / English). It is remembered.

## 2. The window at a glance

| Area | What it does |
|---|---|
| **Menu bar** | File, Project, Edit, Insert, View, Blocks, Electrical, Language, Help |
| **Toolbars** (one each for tools, electrical and 3D, freely placeable) | Drawing tools (Select, Line, Polyline, Circle, Arc, Rectangle, Text, Dimension, Trim, Break) and the electrical tools (Pin, Junction, Cross-ref, Mask, Terminal, Cable, …). Also layer, line type, line weight, colour, unit, scale and zoom. |
| **Side bar** (left, F4 shows/hides it) | Undo / Redo and the sheet list of the project |
| **Drawing area** | This is where you draw. The model is the drawing at 1:1, the layout is the paper sheet. |
| **Input line** | Below the drawing area. Type commands and coordinates here. |
| **Toolbars** | Drawing tools are purple, electrical tools red; zoom has magnifier icons (+, -, "+ G" = zoom extents) and a reset icon. |
| **Status bar** | Mouse coordinates, zoom, layer, selection, hints for the current tool and the switches for object snap, grid and ortho |

The hint in the status bar always tells you what the active tool expects next.
**ESC** cancels the current operation.

## 3. Navigating, snapping, command line

**With the mouse**

- Mouse wheel: zoom (towards the pointer).
- Hold the right mouse button and drag: pan the view.
- Right click without dragging (tool "Select"): context menu.
- Double click with the middle or right button: show everything (zoom extents).
  The **G** key does the same.

**Snapping and aids** (switches in the status bar, also available as keys)

| Key | Function |
|---|---|
| F3 | Object snap (endpoint, midpoint, centre, intersection - also line x circle/arc and circle x circle -, quadrant, perpendicular, nearest) |
| F7 | Show grid |
| F8 | Ortho (horizontal / vertical only) |
| F9 | Grid snap |

**Input line.** You can enter coordinates as `x,y` and type commands, for example
`L` (line), `K` (circle), `REC` (rectangle), `T` (text), `M` (move), `KO` or `CO`
(copy), `RO` (rotate), `AR` (array), `STR` (stretch), `TR` (trim), `BR` (break),
`ZG` (zoom extents), `U` (undo), `B` (create block), `I` (insert block),
`X` (explode block). The commands exist in German and in English.

## 4. Drawing and editing

1. Choose a tool (toolbar or **Insert** menu), click points in the drawing or type
   coordinates in the input line.
2. With the **Select** tool you select objects: click an object or drag a
   rectangle. *Left to right* selects only objects that lie completely inside the
   rectangle. *Right to left* selects everything the rectangle touches. New objects
   are added to the selection; **ESC** clears it.
3. Edit selected objects via the **Edit** menu: copy, cut, paste, duplicate, move,
   copy with base point, rotate, stretch, array, delete (Del).
4. Drag the yellow grips of a selected object to change it.
5. Double clicking an object opens its edit dialog (block attributes, pin, cross
   reference, junction, mask, terminal, cable, coordinate field …). On a viewport it
   activates the viewport.
6. **Undo** (Ctrl+Z) and **Redo** (Ctrl+Y) are also in the side bar.

More drawing aids: **dimensions** (including radius and diameter), **hatch
selection** (Insert menu), **layers** ("Layers…" button) and colour, line type and
line weight in the toolbar.

**Find and replace (Ctrl+F, Edit > Find and replace, command `FIND`):** enter the search text and the new text and choose the scope *Current sheet*, *Whole project* or **Selection only** (searches and replaces only in the objects selected beforehand; if something is selected when the window opens, the scope is already set to it). KatieCAD lists all hits with sheet, object type and field and shows the new text next to it. It searches texts, dimension texts, cross references, masks (IND/TYP/PER ...), terminals, cables, pins and block attributes (so also the designation of devices). **Double-click a hit** to jump to the object: KatieCAD opens the sheet if needed, selects the object and zooms to it; the search window stays open and moves aside. Optional: match case, whole words only. *Replace selected* changes only the highlighted rows, *Replace all* all of them. Changes in the open sheet can be undone with Ctrl+Z; changes in other sheets are saved immediately and cannot be undone there (KatieCAD asks first).

**Match properties (Edit > Match properties, command `MA`):** click the source object first, then the target objects one after another. Layer, colour, line type and line weight are copied; for texts also height and font, for hatches angle and spacing. ESC or right-click ends.

**Own fonts (View > Manage fonts...):** choose any font installed on this computer (TrueType/OpenType); it then appears next to the seven standard fonts in the font list of the toolbar, the text dialog and the properties. The choice is saved; to **remove** a font deselect it in the same window ("Selected only" shows just the active ones, "Deselect all" clears the list). Text width is calculated with the real character widths of the font, and the **PDF embeds the fonts** (readable on computers without the font). Fonts marked "(screen only)" (e.g. OTF with CFF outlines) or with an embedding restriction appear in Helvetica in the PDF. If you open a drawing that uses a font installed here but not chosen, it is switched on for the session automatically; if it is missing completely, KatieCAD shows a substitute font. The stroke font of 3D texts is not affected.

**Colour scheme (View > Colour scheme):** menus, toolbars, side bars and dialogs come in three colour schemes: **Violet** (default), **Black** and **Light**. The change takes effect at once and is remembered for the next start. The drawing background is not touched (set it with *Background*, so choose a light one there). **The background (model and layout) is purely a program setting:** it is stored on your computer and no longer in the drawing or project file; a file saved by someone with a white background opens with your own background (old files are read the same way, their stored background is ignored); drawing content, layers and printed/PDF output do not change. Dialogs that are already open take the new scheme the next time they are opened.

**Toolbar:** the tools are icons (drawing purple, electrical red). Rest the mouse on an icon to see its name. The active tool has a lighter background.

**Offset (Edit > Offset, commands `OFFSET` / `O`):** enter the distance, click an object, then click the side where the copy is to be created. Works with lines, circles, arcs, rectangles and polylines (corners are mitred). If the distance is too large (inwards), KatieCAD says "not possible".

**Change length (Edit > Change length, toolbar, command `LAENGE`):** click the line near the end that is to change. Then either click the new end (it is projected onto the line direction, object snap works) or type the change in the input line: `+5` lengthens by 5, `-5` shortens by 5, `=50` sets the length to 50 (project unit). Then click the next line or ESC.

**Align at two points (Edit > Align > At two points, command `ALIGN` / `AUSRICHTEN` / `AL`, as in AutoCAD):** select objects (Enter), then **1st source point** (a point on the object) → **1st destination point**, **2nd source point** → **2nd destination point**. With one point pair only (Enter at the 2nd source point) the objects are simply moved; with two pairs they are also rotated about the 1st destination point so that the line source 1-2 points along destination 1-2. Finally the program asks "Scale objects based on alignment points?" (default **No**); with **Yes** they are scaled so that both distances are equal. Object snap, ortho and typed coordinates work as for Move, a preview shows the result; locked in 3D.

**Align edges (Edit > Align, commands `AUSLINKS`, `AUSRECHTS`, `AUSOBEN`, `AUSUNTEN`, `AUSMITTEH`, `AUSMITTEV`):** select at least two objects; they are moved to the left/right/top/bottom edge or the centre of the whole selection box.

**Manipulator (Edit > Manipulator, toolbar, command `MANIP`):** switches an axis cross on the selection on/off. Click the **red X arrow** or the **green Y arrow**: the object moves only along that axis. When you click the target point only its component along the axis counts - even if the object snap hits a point beside the axis, the device stays on its line. Or type the distance (`25`, `-10`). The **yellow square** moves freely. ESC cancels.

**3D wireframe (toolbar group "3D:" after Electrical, menu 3D, command `3D`):** the 3D symbol (cube) switches the drawing area to the 3D view in the same window - click again to go back; 2D tools are locked in 3D. Undo/redo, layer, colour, line weight and all other functions of the main window work unchanged. In 3D the 2D drawing lies flat on the ground plane (z = 0); 3D bodies are shown as a plain wireframe (in 2D as a top view).
- **View:** middle mouse button = orbit, **Ctrl + middle mouse button** (or drag with the right button) = pan, wheel = zoom, double-click middle button = "Show all". The **view cube** (top right, can be shown/hidden) sets Top/Bottom/Front/Back/Left/Right by clicking a face; the four **arrows** around the cube step to the neighbouring views; dragging in the cube orbits freely. The icons at the top of the 3D area toggle view cube, perspective and **grid**, set the isometric view and show all.
- **Layer, colour, weight in 3D:** the bar with layer, colour and weight works here too; **double-click** an object to open its size dialog (bodies/sketches) or its properties, **right-click** (without dragging) opens a menu: properties, change size, **copy**, **hide layer of this object**, show all layers, manage layers, delete. **Copy** (also for control cabinets and all other 3D bodies): the copy hangs on the mouse as a yellow preview, object snap catches the corners of other objects, a click puts it down; right-click > Copy again for more copies, Esc cancels, Ctrl+Z undoes it. **To another sheet:** select the objects, Ctrl+C (or Ctrl+X), switch sheet, press Ctrl+V in the 3D view - the copy hangs on the mouse, a click puts it down. This lets you hide objects that are in the way without switching to 2D.
- **Drawing on faces:** with the **normal tools** Line, Polyline, Circle, Rectangle and Dimension of the toolbar (in the 3D view they act automatically on the work plane / as a 3D dimension - there are no duplicate icons) simply move the mouse over a body: the **face under the cursor is highlighted in blue** and the first click draws directly on that face (work plane = this face, yellow with grid and axes). Without a body under the cursor the previous work plane or the ground plane applies. "Pick face" can set a face beforehand; "Work plane = ground plane" switches the automatic face detection off. Radius, width[xdepth] or length can be typed into the "Value" field (Enter; close a polyline with Enter). The sketch can then be **pulled up** (Z arrow or "Extrude", boss on the face), cut into the body as a **bore / pocket** (icon "Hole", depth 0 = through) or pulled downwards (negative value = pocket). A line is open and cannot be extruded.
- **Object snap in 3D (OSNAP):** when drawing on faces and dimensioning, a **visible marker** with a label shows the snap point under the cursor: square = endpoint (body corners, line/sketch ends, circle quadrant points), triangle = midpoint (edge midpoints), circle with cross = centre (circles, caps of cylinders/cones/spheres), cross = grid point. Dimensions snap to all of them in space; drawing snaps to the points lying in the drawing plane.
- **Object snap when placing and moving (OSNAP, F3):** when placing a body/block (the preview follows the mouse) its corners and edge midpoints snap to snap points of existing objects (yellow square with label), so cabinets can be lined up or stacked exactly. When dragging a manipulator arrow (X/Y/Z) a corner of the selection snaps to the coordinate of a snap point of other objects. For blocks the outer edges count (thin parts such as door, handle and mounting plate do not). Without OSNAP only the grid applies.
- **Colour picker with RAL (wherever a colour is chosen):** own dialog in the KatieCAD design instead of the system window. On the left the **RAL Classic palette** (filter by group 1xxx yellow … 9xxx white/black, hovering shows number and name), on the right entry of the **RAL number** (four digits, e.g. `5015` sky blue, `3020` traffic red; with or without "RAL"; while typing the palette shows the matching colours, Enter applies without closing the dialog), the **hex value** or **red/green/blue**; for free colours the most similar RAL is shown. Third tab **"ACI (AutoCAD)"** with the AutoCAD Color Index 1-255 (enter the **ACI number** on the right or click the table; 1 red, 2 yellow, 3 green, 4 cyan, 5 blue, 6 magenta, 7 white/black, 10-249 hues, 250-255 grey); DXF export uses the most similar ACI colour. Second tab **"Colour field"**: hue strip plus a saturation/value square, with number fields **hue 0-360** (e.g. 10 = red, 140 = green, 240 = blue), **saturation** and **value 0-100**. RAL values are screen approximations. "System colour picker ..." opens the operating-system dialog if needed.
- **Grid in 3D:** the same switch as in 2D applies (status bar "Grid", F7, icon in the 3D area). The status bar button "Dotted" shows the grid - also on the ground plane and the work plane - as dots instead of lines.
- **Pull up like AutoCAD:** draw a rectangle, circle or closed polyline in 2D, select it in 3D and drag the **blue Z arrow** up or down (or click the arrow, type the height in the "Value" field, Enter).
- **Selecting with a window (like 2D):** click and drag on empty space. From **left to right** (cyan) only fully enclosed objects are selected, from **right to left** (green) all that the window touches; hits light up magenta beforehand. Shift/Ctrl + window adds to the selection, a plain click on empty space clears it. Orbit/pan stay on the middle button or Ctrl+middle button and the right button.
- **Stretch in 3D (Edit > Stretch, command `STRETCH` / `ST`, as in 2D):** select 3D objects (also cabinets), start the command, **click the base point on the side that is to move** (e.g. on the top edge; corners, midpoints and centres snap), then **click the target point or type the distance** (e.g. `200`, Enter - it stretches towards the side where the mouse is relative to the base point; `-200` reverses). The axis is the main direction of the mouse movement; the preview shows the result in yellow. The side of the base point moves by the distance: large parts (carcass, door, side panels) become longer or shorter, small parts on that side (rails, fittings) move along, everything else stays. Bodies on work planes, spheres, merged bodies and bodies with cut-outs cannot be stretched - they stay unchanged (the message counts them). Ctrl+Z undoes it.
- **Rotate (icon "Rotate", menu 3D > Rotate about axis..., `3DDREHEN`):** rotates the selection about the X, Y or Z axis through the manipulator origin (angle in degrees, positive = counter-clockwise). 3D bodies, blocks, sketches and 3D dimensions rotate about any axis, 2D shapes only about Z. Vertical bores move with the body.
- **Round edges (icon "Round edges", `3DABRUNDEN`):** dialog with a radius and the choice of **top edges** (rim of the top face, "ground off from above"), **bottom edges** and/or **vertical edges** (corners seen from above). Works for boxes, prisms and cylinders (vertical edges only for bodies with corners); too large radii are limited. The rounding shows as layer lines in the wireframe.
- **Move the manipulator:** click the small **orange circle** diagonally below the yellow square (or the icon "Move manipulator", `3DPIVOT`), then click a point (corners, midpoints, centres snap) - the manipulator then sits there and is the pivot for rotating. It follows the object and returns to the centre for a new selection (or menu 3D > Centre manipulator). **In 2D:** also click the orange circle (or Edit > Move manipulator), then click the new origin (object snap works); "Centre manipulator" restores the middle.
- **Cut-outs in the 2D view:** cut-outs that are not open to the top (side faces, underside) appear **dashed** (hidden) in the plan view; holes open to the top stay solid. If several bodies have faces in the same plane, the bore is cut into the body whose face contains the sketch.
- **3D manipulator:** the arrows X (red), Y (green), Z (blue) move the selection along that axis only; with snap on the distance snaps to the grid. With the icon "Z arrow changes height" the Z arrow changes the height of a prism/pyramid instead of moving it. **Exact distance:** while dragging an arrow (mouse button held) just type the number, e.g. `300` (Backspace deletes, `-` for the opposite direction) and confirm with **Enter**: the body moves by exactly that amount (in the selected unit) along the axis; the mouse is ignored meanwhile. It also works after clicking an arrow without dragging: type the number, Enter - or write the number into the input line at the bottom or the "Value" field.
- **Direct bodies:** box, cylinder, cone, pyramid, sphere (icons, menu 3D or commands `BOX`, `CYLINDER`, `CONE`, `PYRAMID`, `SPHERE`). Enter size and position in the dialog or pick the position on the ground plane (view at an angle or from above for this).
- **Control cabinet (icon "Control cabinet", menu 3D, command `CABINET`):** ready-made block of simple bodies. In the dialog pick a common size from the list (11 standard sizes from compact to floor-standing, given as width x height x depth) or "Free dimensions"; the values stay editable. Optionally **with/without mounting plate** (size matches the cabinet; freely adjustable for free dimensions) optionally a **door** (with a rectangular handle and lock, handle on the right or left) and **left/right side panel** (thin sheets, slightly inset so they are visible in the wireframe) and a **plinth** (none, 100, 150 or 200 mm) as a box under the cabinet. The front faces forward (-Y), the mounting plate sits at the back. The block can be moved, rotated and dissolved like any 3D block (parts: plinth, cabinet, mounting plate).
- **Change size afterwards (`3DMASS`, double-click):** select a body or sketch - change width, depth, height, radius (free shapes: scale in %).
- **3D dimensions:** icon "3D dimension", click two points (body corners snap), then the position of the dimension line. It works from any view direction without switching to 2D; in 2D it appears projected.
- **Text in 3D:** the "Text" tool of the toolbar (automatically 3D text in 3D): move the mouse over a body face (the face is highlighted, snapping works), click a point, enter text, text height and angle within the face in the dialog (line break with ` | `). The text **lies on the chosen face or work plane** (like the 3D lines) as simple stroke text; its lower left corner sits at the clicked point. **Double-click** edits it; move/rotate/delete work as for other objects. In 2D it appears as ordinary text on top faces and as lines on vertical faces.
- **Distance in 3D (`MEASURE`, `DI`):** in the 3D view MEASURE gives the distance of two space points (snapping to corners/midpoints/centres) and shows distance plus dX, dY, dZ in the status bar - without creating a dimension. Measure further point pairs; ESC ends (the measuring lines then disappear).
- **Properties (double-click):** line with a **Length** field (changing it moves the end point, point 1 stays); rectangle with **Width/Height** and resizing from corner 1 or on both sides about the centre.
- **Typing while drawing in 3D:** the **input line** at the bottom works as in 2D: first point as `x,y` on the work plane, then circle = radius, rectangle = `width,height` (or `width x height`), line = length or `length<angle`, polyline = `x,y` or `@dx,dy` (Enter on an empty line closes). Alternatively the "Value" field in the 3D area. **OSNAP (F3)** and **ORTHO (F8)** also apply in 3D: without OSNAP only the grid snaps; ORTHO restricts lines/polylines to the face's X or Y direction and dimensions/distances to one space axis.
- **2D functions in 3D:** Arc, Ellipse, Spline, Trim, Break, the electrical tools as well as Length, Fillet/Chamfer, Offset and Align are **greyed out and locked** in the 3D view (message "2D only") - you stay in 3D and can use them after switching back.
- **3D in a viewport (layout):** click a viewport and press the 3D icon in the layout - the viewport shows the model as an isometric wireframe (the layout stays, the 3D window no longer replaces it). Activate the viewport by double click (a double click into another viewport switches straight to it, a double click outside leaves the viewport view - so every viewport can show its own view), then **drag with the middle mouse button = rotate**, right button = pan, wheel = zoom. Right-click > "3D view in this viewport" offers standard views (isometric, top, front ...) or takes the camera of the 3D view. The viewport is printed to scale and exported to PDF. Pressing the 3D icon again or "Back to the 2D view" restores the normal state.
- **3D block:** select several 3D bodies › icon "Make 3D block" (`3DBLOCK`); the block is selected and moved as one unit. It is for overview only and has no electrical function. "Dissolve 3D block" splits it again.
- **Merge 3D bodies (menu 3D, command `3DVERSCHMELZEN` / `3DUNION`, right-click > "Merge bodies"):** select at least two 3D bodies (also whole 3D blocks such as cabinets). They are united into **one** body (boolean union): overlaps and edges inside disappear, only the common outer skin remains; holes and cut-outs of the parts are kept. The new body can be moved, rotated, scaled, copied and deleted like any other, is saved with the project, and works with "Hide hidden edges" and in the PDF. **Limits:** the parts can no longer be edited individually (pulling the height, holes and rounding are not possible for the merged body, size only by factor; Ctrl+Z restores the single bodies). Round bodies are merged as polygons (smooth transitions are not drawn as edges, the lines of the original bodies are kept). Bodies that do not touch are still combined into one object (with separate parts). A cabinet becomes a plain outer shell - the mounting plate inside disappears.
- **Hide hidden edges:** the button *Hide hidden edges* in the 3D bar (cube with dashed back edges) shows the bodies like a solid model: edges covered by a body in front disappear (there are deliberately no dashed back edges), and a cabinet has only one possible reading. A **cabinet without a door is open at the front**, also without a mounting plate: the interior (and the mounting plate, if any) stay visible, also when the cabinet is rotated. While turning, panning and zooming KatieCAD shows the full wireframe for speed and recalculates afterwards. Selected bodies are highlighted along their visible edges only.
- **Hidden edges in the layout and in the PDF:** in the layout the same setting exists per viewport: right-click the viewport > *3D view in this viewport* > *Hide hidden edges* (tick = on). It is stored with the project, stays when the standard view changes and also applies to the PDF output. "Take camera from 3D view" takes the state of the 3D button along. So a cabinet can be set up once in 3D, hidden-line and printed cleanly.
- **Hide cabinet doors per viewport (since 1.1.3):** right-click the viewport > *3D view in this viewport* > *Hide cabinet doors* (tick = on). Door, handle and lock of all cabinets disappear in this viewport only; the model itself is unchanged. A cabinet with a mounting plate can thus appear in the same layout once with and once without door, without drawing it twice (viewport 1: front with door, viewport 2: open with mounting plate, viewport 3: side). A cabinet without door is open at the front (see hidden edges). The setting is saved, applies to object snap, dimensioning and PDF output, and stays when the standard view changes.
- **View cube and "Hidden" button in the layout:** a 3D viewport that is **selected or active** (turning on "3D view" selects it automatically) shows the view cube with rotation arrows at the top right: a click on a cube face sets the standard view (Top, Front, Left ...), the arrows turn in 90°/45° steps, dragging the cube rotates freely. Below it the **Hidden** button (tick = on) toggles hidden edges of this viewport - the same setting as in the right-click menu. The cube appears on screen only, never in print or PDF, and only in viewports that are large enough. Every change can be undone with Ctrl+Z.
- **Move and copy from point to point in 3D:** select object(s), then click *Move from point to point* in the 3D bar (or Edit > Move (base point), or command `V`/`M`, copy with `CO` - in the 3D window they now work in space). First click the **base point**, e.g. a corner of the cabinet, then the **target point**, e.g. the corner of another object. With object snap on (F3) both points snap to **corners, edge midpoints and centres** (yellow marker with label); ORTHO (F8) restricts the move to one axis. While you aim, a dashed preview shows the moved selection with the distance. ESC cancels, Ctrl+Z undoes. Both are also in the **right-click menu** (*Move with base point*, *Copy with base point*). Dragging the manipulator axes still snaps axis-wise. **Limits:** snap points are corners, midpoints and centres; edge intersections rarely exist in space (two lines almost never meet exactly) and are not snapped.
- **Object snap in the layout on viewport content:** in the layout, line, dimension, text and all other tools now also snap to points **inside viewports**, without having to activate the viewport. In **2D viewports** all snap kinds of the model apply (endpoint, midpoint, centre, quadrant, intersection ...), in **3D viewports** the **corners, edge midpoints and centres** of the bodies in the view shown (with hidden edges on, only points on visible edges). Objects of the layout itself take priority. The snap kinds can be switched off individually as usual (F3 switches all off). A **dimension in the layout** whose points lie in a viewport now shows the **model value** (paper distance divided by the viewport scale) instead of paper millimetres; so a cabinet built in 3D can be dimensioned to scale in the layout. If the points are outside a viewport the paper measure stays; "override text" changes the value at any time. Angle dimensions are not affected.
- **Hide terminal fields:** in the terminal dialog (placing and double-click) every field (IND, MAN, TYP, PER, NUM) has the *show* check box, as with devices. Hidden fields do not appear in the drawing but stay available for the terminal plan, device list and parts list; the visible lines move up. The same applies to the device mask. The choice is kept while you place several terminals in a row.
- **Window size:** the main window has a minimum size (1010 × 600 pixels, the screen size on smaller screens) so that toolbars, status bar and input line always stay usable.
- **True measures in a viewport:** a dimension in the layout measures the **projection** of the points on paper. It only shows the true length if the view is aligned exactly to an axis (Front, Back, Left, Right, Top, Bottom) and not perspective. A few degrees of tilt already falsify the measure (e.g. 150 mm plinth -> 149.70 mm, and points at different depths, such as front and rear edge, shift against each other). So when turning a viewport (middle mouse button or view cube) the view **snaps exactly onto a standard direction when within 4 degrees**. For a view that is already tilted: right-click > *3D view in this viewport* > *Front* (etc.).
- **Right-click in the layout over a viewport:** if an object lies under the pointer (dimension, text, line ...), its menu opens with *Move (base point)*, *Copy (base point, multiple)* and *Copy with base point*; the viewport menu only appears on the free viewport. The viewport menu itself now has the same three entries for the viewport frame.
- **Dimension text and other properties of the dimension:** double-click a dimension (or right-click > Properties, Ctrl+1) opens the properties of the dimension - including the field *Displayed text* with the measured value next to it. It may contain any text, e.g. **150**, even if the measure is something else; `<>` stands for the measured value ("<> mm", "approx. <>"); *Restore measured value* (or an empty field) shows the measured value again. The command `MASSTEXT` opens the same properties. The text is saved with the drawing, appears in the PDF and Ctrl+Z undoes it. **Text height, font, arrow size and end piece** (*Arrow* or *Diagonal tick* - the diagonal stroke of architectural dimensioning; for new dimensions also in the toolbar) are set there too; in the properties window (Ctrl+1) this also works for several dimensions at once (the text angle stays locked for dimensions, it follows the measuring direction). **Decimal places** (0 to 6, e.g. 800 or 800.0000) are set there as well or via right-click > *Decimal places*; new dimensions use the value in the toolbar.
- Everything else stays a simple wireframe (no faces, no rendering).

**Placing the toolbars (View > Toolbars, or drag the grip ⋮⋮):** there is one bar each for **Tools**, **Electrical** and **3D**. The ☰ button that shows/hides the sidebar has a fixed place at the **bottom left** of the status bar (also F4) and stays visible while the sidebar is hidden. Each can be docked separately at the top, bottom or right - drag the grip at the start of the bar to the desired window edge and release, it snaps there. At the top/bottom the bars sit side by side and wrap into a new row in a narrow window; at the right the symbols wrap into several columns. The **order** is changed via View > Toolbars > "Move forward / back" or by dropping the grip on another bar (e.g. Electrical before Tools). The choice is saved per bar.

**Quick select (Edit > Quick select, command `QS`):** selects all objects of one object type, layer, colour or line type. Several criteria apply together (AND). Optionally select everything except the matches or add to the current selection.

**Chain dimension (Insert > Chain dimension, command `KETTE`):** two measurement points and the position of the dimension line as with the normal dimension; after that one click per further point is enough, and every new dimension starts at the last point on the same dimension line. ESC or right-click ends.

**Measure (Edit > Measure, commands `MEASURE` / `DI`):** click two points (object snap works). KatieCAD shows distance, dX, dY and angle in the status bar and draws the measured segment. Further clicks start a new measurement, ESC or right-click ends. Values use the current unit.

**Fillet and chamfer (Edit > Fillet / Chamfer, commands `FILLET` or `F`, `CHAMFER`):** enter the radius or the chamfer distances, then click two lines one after the other. The lines are trimmed (or extended) at the corner and joined by an arc or a chamfer line; the longer side of each line is kept. Radius 0 / distance 0 just closes the corner. You can also click a **rectangle or polyline**: a click on a corner rounds only that corner, a click on an edge rounds all corners; the object is split into lines and true arcs. Parallel lines or a radius that is too large give "not possible". The dialog remembers the last values; ESC ends.

**Ellipse and spline (Insert > Ellipse / Spline, commands `ELLIPSE`, `SPLINE`):** *Ellipse:* centre, end of the first axis, then the length of the second semi-axis (click or coordinates in the input line). Grips change centre and both semi-axes; rotate, scale and mirror work as well. *Spline:* place the support points one after another, the curve runs smoothly through all of them; Enter or right-click finishes, a click on the start point closes the curve. Every support point has a grip. DXF export writes both as polylines (imported DXF ellipses/splines stay polylines). Inside blocks / when exploded they become plain polylines.

**Rooms (Insert > Room, "Room" button, command `ROOM`; since 1.1.3):** Click the **corners of the room** one after another (any number, also L- or U-shaped, with object snap on the inner wall corners if you like); a click on the first point (or Enter / right click) closes the room. Then enter room number and room name. Below them the **area in m²** appears, calculated automatically (drawing unit mm). The box is **invisible** - only the text is shown. Clicking the text selects the room and shows the box with **corner grips**: use them to change the room size (the area is recalculated); the centre grip moves the text only. Double click on the text (or right click > *Edit room*) changes number, name, **font** (also bold) and text height. Rooms are on the layer "Räume" (can be hidden); PDF and DXF contain the text only.

**Walls, doors and windows (Insert > Wall / Door in wall / Window in wall, commands `WALL`, `DOOR`, `WINDOW`; since 1.1.3):** For building floor plans, 2D only. *Wall:* the tool first asks for the **wall thickness** (mm) and the **position of the drawn line** (wall centre, left or right face). Then click the corner points one after another (or type coordinates or length and angle in the input line); Enter or right click finishes, a click on the start point (or `S`) closes a room. The wall appears with both faces and mitred corners on its **own layer "Wände"**, created automatically. It can be moved, rotated, scaled, mirrored and copied like any object, has object snap on all edges and corners (for dimensioning) and is selected by clicking the wall body; **double click** changes thickness, position of the line and the **hatch** (none, diagonal 45°, cross or **solid fill**; line spacing adjustable, default 180 mm) - the hatch fills the wall body only, leaves door and window openings free and needs no hatch command; right-click > *Hatch wall (on/off)* or the command `WALLHATCH` does it with one click. **Joining walls:** the *Join walls* button in the toolbar (or *Insert > Join walls*), then click the two walls one after another - they are merged at once. Alternatively select two walls and use right click > *Join walls* or the command `WALLJOIN`. Both walls are merged at their nearest ends into **one** wall with a clean mitred corner: the centre lines are extended or trimmed to their common intersection, also for two opposite ends in line (a small gap is bridged). Doors and windows keep their look. Not possible: closed walls (rooms), parallel walls far apart and ends too far from the corner point (a message appears); **Close wall:** click the same wall a second time (or select a wall > right click > *Close wall*): start and end are joined into a clean mitred corner and the wall is closed. **T junction:** if the end of one wall is in front of or in the middle of the other, it is extended or trimmed onto its centre line (the two walls stay). **Walls that touch or overlap automatically form one common outline:** wall faces and hatch inside another wall are not drawn. With **Ortho (F8)** wall points can also be dragged by their grips horizontally/vertically relative to the neighbouring point. (The "Change length" button next to it is a separate, older tool and has nothing to do with walls.) *Door models:* choosing "Door" or "Window" first shows the **properties window** (the values apply to all following clicks); for doors choose the **model**: *Single leaf*, *Double door* (two equal leaves), *Double door with a larger leaf* (share in % adjustable; the tick "Large leaf on the other side" swaps the side) or *Roller shutter* (dashed line in the wall opening, no leaf). Usual sizes are suggested when the model changes. *Doors and windows* are **objects of their own, completely normal:** choose the tool and click on the wall - the object sits there and follows direction and thickness of the wall; a door automatically cuts the gap into the wall. Afterwards they can be **selected, moved (centre grip or Move with base point), copied, mirrored, rotated and deleted like any object**; the two end grips change the width. **Double click on a door/window** opens only its own properties: width, height (windows also sill) and, for doors, the ticks *Hinge on the other side* and *Door opens to the other side of the wall*. The same two switches are in the right-click menu. A wall can have any number of doors and windows. DXF and PDF output everything as lines; saved as a block, wall, doors and windows become plain lines. In the 3D view the wall tools are locked (like the other 2D tools).

**Angle dimension (Insert > Angle dimension (3 points) / (2 lines), commands `ANGULAR`, `WINKELLINIEN`):** *3 points:* vertex, point on the first leg, point on the second leg, then click the position of the dimension arc. *2 lines:* click both lines (the vertex is their intersection, the clicked side selects the leg), then place the arc. The angle sector is the one that contains the dimension arc, so angles above 180° can be dimensioned too. Grips for vertex, both legs, arc and text; text height, arrow and decimals work like the other dimensions.

**Purge layers:** in the layer window ("Layers...") **Purge** deletes all layers no object uses - in a project across all sheets (also layouts and blocks). Layer 0 and the active layer stay. KatieCAD asks first with the list. Ctrl+Z undoes it only for the open sheet; the other sheets are saved immediately.

**Hatching like AutoCAD:** with nothing selected, choose Insert > Hatch, set pattern, spacing and angle, then click straight into an enclosed area. KatieCAD finds the smallest region around the click point (lines may cross; circles, rectangles and polylines count too) and hatches it. Click several areas one after another; ESC or right-click ends. If a closed boundary is already selected, that one is hatched as before.

**Stretch with a preselection:** if you selected objects beforehand with a crossing window (right-to-left), **Stretch** (`STR`) jumps straight to the base point - no second window needed. Only the selected objects are stretched. With another kind of preselection (e.g. single click) the selection is kept and you only drag the window.

## 5. Projects and sheets

A **project** is a folder with a project file (`*.katieprj`), one file per sheet
(`Blatt_001.cadjson` …) and a folder `Bloecke` for block files.

**Project** menu:

- **Create project…**: choose a name and location. The first sheet is created.
- **Open / save / close / rename… / delete project…**
- **New sheet, duplicate sheet, sheet properties (F2: name and installation location), delete sheet**
- **Print sheets / as PDF…**
- **Create / update documentation…** and **Export lists as CSV…** (see section 9)

In the **side bar**, one click switches the sheet. The current sheet is saved
automatically. A double click renames a sheet. Select several sheets with **Ctrl** or **Shift** + click
to move them together with the arrow buttons or delete them with "−" (while several
sheets are selected, the current sheet stays open). Undo is kept per sheet.

Without a project you work on a single drawing (**File** menu: New, Open, Save …).

## 6. Model, layout, frame, printing

- **Model** (**View** menu): the actual drawing in full size (mm).
- **Layout**: the paper sheet (e.g. DIN A4 landscape). It holds the frame, the title
  block and **viewports**, which are windows onto the model with their own scale.
  Create a viewport with **Insert > Place viewport**.
- **Insert > Frame + title block…**: places the sheet margin and a title block from a
  template. Your own title blocks are ordinary drawings (`*.cadjson`) in the folder
  `title_blocks/`; their origin is the lower right corner of the sheet frame.
  Fields such as `PAGE`, `PAGES`, `SHEET`, `PROJECT`, `DATE`, `SCALE`, `FORMAT` are
  filled in automatically. With **Project > Project properties…** you enter customer,
  drawn by / checked by, drawing number and the revision table (4 rows: index, change,
  name, date) once; they appear in the title blocks of all sheets. The title is made of
  customer, project name and sheet name; the paper format follows the layout format.
  The field names (e.g. `CUSTOMER`, `DRAWN`, `REV1_INDEX`) are listed in
  `title_blocks/README.md`.
- **Insert > Save drawing as title block template…** turns a drawing into a new
  template.
- **File > Print** (Ctrl+P) and **Project > Print sheets / as PDF…** create a PDF
  (several sheets in one file) or open the print preview.

## 7. Blocks and attributes

A **block** is a reusable group of objects (for example a symbol). **Blocks** menu:

- **Create block (B)**: select objects, press `B`, click the base point, choose a
  name and a save location.
- **Insert block/device (I)** opens the block browser. A double click on a block places it
  in the drawing. Blocks are ordinary files (`*.katieblock`) in the folders shown by
  the browser (including the project folder `Bloecke`).
- **Explode block (X)** breaks a block apart again.
- **Save block/device to file / load block from file** (one shared entry in the Blocks menu; the duplicate entry in the Electrical menu is gone).
- **Define attribute (ATTDEF)**: a text field inside the symbol whose value differs
  per inserted block. Select it together with the symbol geometry and create the
  block. KatieCAD asks for the values on insertion. **Edit attributes (ATTEDIT)**
  changes them later. For devices with very many pins (e.g. 16-channel PLC modules) the list in the window is **scrollable** (mouse wheel or bar on the right); OK and Cancel always stay visible.

## 8. Electrical: drawing a schematic

All tools are in the **Electrical** menu and in the toolbar.

**Automatic layers:** electrical objects no longer go to layer 0 but to layers KatieCAD creates on demand: **E_DEVICES** (devices), **E_LINES** (wires, junctions, cross references), **E_CABLE** (cable definitions), **E_CLAMPS** (terminals) and **E_PIN** (single pins as long as they are not combined into a device; inside a device they belong to E_DEVICES). Existing objects stay unchanged; the layers can be hidden or recoloured like any other.

### Building blocks

| Element | Purpose |
|---|---|
| **Pin** (PIN) | Connection point with a label (e.g. `1`, `2`, `A1`). Wires end here. |
| **Electrical mask** (MASKE) | Label field of a device: **IND** (equipment identifier, e.g. `K1`), **TYP** (type), **PER** (description). **REF** fills itself in. |
| **Junction** (VERBINDUNG) | Corner, T-piece or crossing. In the dialog tick the directions (North/West/East/South) that get a wire connection (at least 2) and optionally "With dot" (= electrically connected). The dot also works for a T-piece with 3 directions; a 4-direction crossing without a dot is only a wire crossing. |
| **Cross reference** (QV) | Arrow that continues a current path on another sheet. Same text = belongs together. |
| **Terminal** (KLEMME) | Terminal block with two connections (top/bottom) and the fields IND (terminal strip), TYP, PER, NUM (number). |
| **Cable** (KABEL) | Horizontal line with a label. Where a vertical wire crosses it, a core marker (L1, L2, L3, N, PE …) appears automatically; the designation can be changed. |
| **Coordinate field** (FELD) | Column/row grid of the sheet, so that references can be given as "sheet/column/row". In the dialog choose **DIN A4** (287 × 164 mm, 6 × 4), **DIN A3** (395 × 252.59 mm, 8 × 5) or enter your own values. |
| **Function text** (FTEXT) | Normal multi-line text on the layer **F-Text** (created automatically). It says what the devices and terminals **behind** its insertion point are for. Rule: a device/terminal belongs to the nearest function text **on the same sheet** that lies **to its left (or directly above)**. In the terminal diagram an unchanged text is shown only at the **first** terminal of the strip. The text appears at the far **right** of the device list and the terminal diagram in the column **Function** (the column is dropped when there are no function texts). |

### Ready-made symbols

The block browser (**Blocks > Insert block/device**, key `I`) contains an entry
**symbols** (the symbol library) with basic symbols (contacts, push buttons, fuses, breakers,
coils, motors, components, meters …). A double click places a symbol; mask and pins
are already prepared. The list is in `symbols/README.md`.

### Creating a device

1. Draw the symbol (lines, rectangles …) and attach the **pins**.
2. Place an **electrical mask** next to it. Choose the kind: **main device** (e.g. a
   coil) or **auxiliary device** (e.g. an auxiliary contact).
3. Select symbol, pins and mask **together**. The selection rectangle must also
   contain the whole text of the mask, which lies to the left above the mask's anchor
   point.
4. **Electrical > Create device from selection…**, click the base point, enter a
   name and confirm main/auxiliary device. The device is now a block and is saved
   as a file in the block folder.
5. Place it with **Insert block/device (I)** or **Blocks > Load block/device from file…**.
   On insertion the program asks for IND, MAN, TYP, PER and the pin names.

Devices with the **same IND** belong together: the main device shows the sheets of
all auxiliary devices in REF, an auxiliary device shows the main device. This way you
get, for example, a coil `K1` on sheet 3 and its contacts `K1` on sheets 5 and 6.
Each device may contain only **one** mask. For devices with several contacts, create
each contact as its own auxiliary device.

**Single-pole representation (second drawing):** If you draw the same device once
multi-pole (circuit diagram) and once single-pole (e.g. overview, distribution board
plan), tick **Single-pole representation** in the dialog of the single-pole symbol
(device mask, block, terminal or cable). A symbol marked this way is **not counted
anywhere**: not in the device list, parts list, terminal plan, cable or PLC list, not in
the net (connection and terminal lists), not in cross references/REF, not in the
project check ("main device duplicate") and not in automatic numbering. Give the
single-pole symbol the same identifier (IND) as the multi-pole one so they can be
matched. Note: a device drawn **only** single-pole appears in no list - count it with a
multi-pole symbol - or tick **Project > Evaluate single-pole representation too** (also in the "Create documentation" dialog). Then single-pole symbols are counted, numbered, checked and used in the net like normal symbols, so projects drawn **purely with single-pole symbols** can be evaluated as well. If you draw the same device multi-pole **and** single-pole, leave the tick off, otherwise it shows up twice. The setting is per project and saved with it. If you change the identifier of the multi-pole
symbol, change it in the single-pole one by hand.

**Number of poles:** for your own devices enter it in the same dialog in the field
**Number of poles** (e.g. `3` or `3+N`; the field is active once the tick is set). It is
shown exactly as you type it (`3`, `/3` ...) above the identifier (IND) and can be moved like the other mask texts.
Symbols from the "12 Single-pole" library have the attribute **POLE** instead (a stroke
on the line with the number); then the field does not appear twice.

### Wires

- **Automatic:** if two connection points (pins, junctions, terminals, cross
  references) lie exactly above each other or side by side and their directions
  match, the red wire appears by itself. It disappears again if you remove one of
  the points.
- **By hand:** tool **Draw wire (LEITUNG)**, then click two connections one after the
  other.
- If you place a pin, device, terminal or junction **on** an existing wire, the wire
  is interrupted there and connected.
- Double click a junction to change its directions and dot.

### Across sheets: cross references

**Chain over several sheets:** you do not need `L1.1`, `L1.2` ... With the same name an *outgoing* arrow points to the *incoming* arrow on the **next** sheet, an *incoming* one to the *outgoing* one on the **previous** sheet (left to right, in sheet order). So `L1` can run from sheet 1 over 2 and 3 to 4 and each arrow names only its neighbour. If there is no matching partner in that direction, all other places with this name are shown as before.

At the end of a wire, place a **cross reference** (type *outgoing* or *incoming*,
direction, text, e.g. `L1`) and place one with the same text on the other sheet. The
target (sheet/column/row) is shown automatically. For the lists, KatieCAD follows the
current path across such pairs when there is exactly one outgoing and at least one
incoming arrow with the same text. A potential such as `L1` that occurs in many
places stays an end point.

**Cross-reference texts:** the identifier (e.g. `L1`) and the target note (e.g. "(Sheet 6/1/D)") stand side by side on one line by default and have default heights of 2.5 mm and 1.5 mm. In the cross-reference dialog (double-click) you set both heights separately. Both texts can also be moved with their yellow grips. **Reset text positions** in the dialog puts them back to the default position.

**Moving texts freely:** The labels of terminals, masks (IND/MAN/TYP/PER/REF), cables, pins and device blocks can be moved as well. Select the object and drag the yellow grip at the text. For an inserted device the move applies to that one instance only. **Reset text positions** in the right-click menu puts the texts back to their default position. Since 1.0.3 the terminal number (NUM) is more readable at 1.75 mm.

### Terminals and cables

- Place the terminals side by side. **NUM** counts up by itself on the next
  placement. You only need to enter the terminal strip (IND) on the first terminal of
  a row; the terminals to its right in the same row take it over.
- Place the **cable** with two clicks (start, end) across the vertical wires. The end
  can be extended later with its grip. CAB is the identifier of the cable (e.g. `W1`).

## 9. Generating documentation

**Project > Create / update documentation…** creates ordinary sheets in the
project, in either **DIN A4** or **DIN A3** (chosen in the dialog; on A3 areas, texts and row heights are scaled to fit):

- **cover sheet** and **table of contents** (in front of the drawing sheets)
- **device list**, **terminal diagram** and **cable plan** (behind them)
- **PLC list** (I/O list of all PLC modules: controller, module, slot, type, address, data type, symbol, comment, connection, location). A block is a PLC module if it has the attribute `SPS` = `DI`, `DO`, `AI` or `AO` (the symbols of "10 PLC" do). Fill in the extra fields with **Edit attributes**: `STATION` (controller), `PLATZ` (slot) and per channel `VPn_SYM` (symbol) and `VPn_KOM` (comment). The address is the pin text (e.g. `I0.0`).
- more lists (switch on in the dialog): **connection list** (from/to with cable and core), **parts list** (grouped by TYP with manufacturer, order number, description and designations), **cross reference list**, **potential overview** (L1, N, PE, +24V ... with all connections), **connector overview** (pin assignment of all connectors; connectors are devices with a designation `X...` or a type like "connector"/"plug"), **label list** (devices, terminals, cables for labelling) and **revision overview** (from the revision table in the project properties)

In the dialog you choose the sheets, the title block template and the project data
(plant, customer, order number, drawing number, company, drawn / checked by,
revision, date) and the sheet format. The report sheets are rebuilt completely on every run. Manual
changes in them are lost; your drawing sheets stay untouched.

- **Manufacturer (field `MAN`):** besides IND, TYP and PER the device mask has the field **MAN** (*manufacturer*). Order from top to bottom: **IND, MAN, TYP, PER, REF**. The manufacturer appears in the **device list** (column *Manufacturer*) and in the **parts list**: the MAN field of the device is used first, if it is empty the manufacturer from the parts catalogue for the TYP; the same type from different manufacturers is listed in separate rows. **Terminals and cables** have the field MAN too: on a terminal it is drawn below IND and TYP and PER move down one line; on a cable it sits between CAB and TYP (CAB moves up). This only applies when MAN is filled in, otherwise terminals and cables look as before. The manufacturer appears in the terminal plan, the cable plan, the terminal strip row of the device list and the parts list. **In the lists the columns have readable names:** *ID* (IND), *Manufacturer* (MAN), *Type designation* (TYP) and *Rating* (PER); the drawings keep the short tags. An empty field is not drawn; devices already placed in old projects stay as they are until you enter MAN (double-click the device). **Updating existing symbols:** `python tools/symbole_man_ergaenzen.py` (in the project folder) adds the field MAN to every mask in `symbols/` and changes nothing else; with `--pruefen` it only shows what it would change.
- The lists are built from the masks (IND/MAN/TYP/PER), terminals, cables and the wires
  between them. Locations are given as sheet/column/row.
- **Parts catalogue (Project > Parts catalogue...):** assign manufacturer, order number and description to every TYP. "Take over types from drawing" enters all TYP values found, you only add the details. The parts list uses them automatically. The catalogue is stored in the project file.
- **Number devices automatically (Project > Number devices automatically, command `NUMMERIEREN`):** devices whose designation (IND) is only a prefix (`-K`, `K?`) get the next free number: `-K1`, `-K2` ... Numbers continue after the highest one already used in the whole project; assigned numbers never change. Only the main symbol is numbered, top to bottom and left to right, for the whole project or the current sheet. Auxiliary parts (contacts) are not changed.
- **Export lists as CSV…** writes the same tables for Excel (semicolon separated,
  UTF-8).
- **Export lists as Excel file…** (Project menu): choose the lists (device list, terminal diagram, cable plan, connections, parts list, …; the number in brackets is the row count) and get **one .xlsx file with one sheet per list** (bold frozen header row, filter set, column widths fitted, number columns as numbers, designations such as `001` stay text). Neither Excel nor an extra library is needed; the selection is remembered in the project.
- **Customise columns:** copy `report_templates/geraete.example.json` and rename it
  to `geraete.json`, `klemmen.json`, `kabel.json` or `inhalt.json`. More in
  `report_templates/README.md`.

## 10. Import and export

- **File > Import DXF… / Import DWG…** reads foreign drawings, **Export DXF… / Export DWG…**
  writes them. DXF works directly. DWG import works without extra software (built-in `ezdwg`). For difficult files you can optionally
  install the free **ODA File Converter** (opendesign.com/guestfiles/oda_file_converter);
  KatieCAD then uses it automatically (restart required) and reads more accurately. **Export DWG** needs this converter, **Export DXF** does not.
- **File > Export DXF…** writes the drawing as DXF.
- PDF: see section 6.

## 11. Keyboard shortcuts

| Key | Function |
|---|---|
| Ctrl+S | Save (in a project without prompting) |
| Ctrl+P | Print |
| Ctrl+Z / Ctrl+Y | Undo / Redo |
| Ctrl+C / Ctrl+X / Ctrl+V | Copy / Cut / Paste |
| Ctrl+Shift+C | Copy with base point |
| Ctrl+D | Duplicate (with offset) |
| Ctrl+A | Select all |
| Del | Delete selection |
| ESC | Cancel / clear selection |
| F1 | Window listing all keyboard shortcuts, mouse actions and commands (scrollable, with search; also Help > Keyboard shortcuts and commands) |
| F2 | Sheet properties (name, installation location) |
| F3 / F7 / F8 / F9 | Object snap / show grid / ortho / grid snap |
| F4 | Show / hide side bar |
| Ctrl+B | Insert block/device (block selection) |
| Ctrl+F | Find and replace |
| G | Show everything (zoom extents) |
| B / I / BL / X | Create block / insert / block selection (like I) / explode (in the input line) |

On the Mac, Cmd replaces Ctrl.

## 12. Tips and frequently asked questions

- **"Create device from selection" says the mask is missing:** the mask must be part
  of the selection. Drag the rectangle left to right and large enough to contain its
  whole text. If the mask is already inside a placed block, explode that block first
  (X).
- **A wire is not created:** the connection points must be exactly aligned and their
  directions must match. Switch on object snap (F3) to hit them precisely.
- **The lists show "→ L1" or similar:** the path ends at a cross reference without
  a unique counterpart (or at a potential such as L1). This is intended.
- **Terminals appear without a terminal strip:** enter IND on the first terminal of
  the row; the ones to its right take it over.
- **Only one dialog at a time:** opening a new dialog closes the previous one.
- **Safety:** drawing sheets are saved automatically when you switch sheets. Use
  Ctrl+S to save the project at any time.

**Linux - menu bar:** on Linux KatieCAD draws its own menu bar (a click opens it; a click elsewhere, ESC or switching to another program closes it; F10 and the arrow keys work). To get the standard Tk menus start with `KATIECAD_NATIVE_MENU=1 python3 main.py`.

## Project check / contact mirror
**Project › Check project…** checks all drawing sheets: duplicate main devices and cables, auxiliary parts without a main device, duplicate terminals, cross references that occur more than twice / have no counterpart / use the same arrow type twice, and open terminal connections. Double-click a finding to jump to it. Mark cross references that intentionally have no counterpart (supply, handover) with **Handover / external** in the cross-reference dialog. Such references point nowhere and are never targeted by others: the same text (e.g. `L1`) may appear any number of times, no need for `L1.1`, `L2.1` ... The potential overview still lists them.

**Contact mirror:** In the device dialog (edit attributes or device mask) choose *Display*: reference list, contact mirror right of the symbol, or - for relays - below. The contacts are taken from the auxiliary parts with the same identifier; make/break/changeover is derived from the pin labels (13/14, 21/22, 11/12/14 ...).

**Moving the contact mirror:** Select the device - a yellow grip appears at the upper left of the mirror. Drag it to move the mirror freely; the position stays relative to the device. It is reset when the display mode is changed.

## Properties (Ctrl+1)
**By layer (colour and weight):** the colour area of the toolbar has a **By layer** check box next to the colour field, and the colour dialog has a **By layer** button: new objects then take the colour of the current layer (the colour field shows it). In the **Weight** list **By layer** is the first entry: the line weight then comes from the layer and follows it. With a selection, changing the weight applies it to existing objects too; the properties window (double-click) and the properties palette (Ctrl+1) offer the same "By layer" choice.

Edit › Properties opens a window for the current selection, also mixed (lines, texts, symbols ...): layer, colour (or "By layer"), linetype, line weight and - as soon as texts are included - text height, angle and font. Differing values show as *VARIES*; a change applies at once to all selected objects.

## Scale and mirror
**Edit › Scale** (command `SCALE`/`SC`, also in the right-click menu): select objects, Enter, pick the base point, enter the factor (e.g. `2` or `0.5`). Blocks are scaled with their size; fixed-size electrical elements (junctions, cross references, masks, terminals) keep their size and only move to the new position.

**Edit › Mirror** (command `MIRROR`/`MI`, also in the right-click menu): select objects, Enter, pick two points of the mirror line (live preview), then decide whether the originals are deleted. Texts stay readable (not mirrored); blocks including pins and labels are mirrored correctly and remain devices.

## Whole project as one DXF file
**Project › Export project as one DXF…** evaluates all sheets like printing (layout with frame, title block and viewports) and places them side by side in one DXF file: 4 sheets per row, then a new row. Every sheet is on its own layer (`Blatt_01` ...), plus `Blattgrenze` and `Blattnamen`.

## Info window and log
Help › About shows the logo, version and license. **License** opens the license text; **Log** opens the log file (`katiecad-log.txt` in the KatieCAD settings folder) in your default text editor – useful for error reports. The previous session's log is kept as `katiecad-log.txt.old`.

## Installation location (sheet properties)
Press **F2**, double-click a sheet or right-click > *Sheet properties…* to set the sheet name and its **installation location** (e.g. "Panel UV1"). It applies to every object on the sheet automatically and is not copied into the objects: change it and the title block and lists follow at once. In the title block an attribute with the tag `PLACE` (German `EINBAUORT`) shows it. The device, terminal and cable lists get a *Location* column (only if at least one sheet has a location); the same equipment identifier at different locations counts as different devices. Report sheets have no location.

Dimensions: **Insert > Radius dimension (DR)** and **Diameter dimension (DD)** - click a circle or arc, then the text position.

## Terminal diagram: bridges
Column order: terminal strip, location, type, **connection top, terminal (NUM), bridge, connection bottom**, sheet/column/row. Terminals of the same strip that you wire together on the top or bottom side count as a bridge: the *Bridge* column shows a line with dots at the connected terminals (overlapping bridges use separate lanes). The target then appears only on the first terminal of the bridge; the other cells stay empty. The column only appears if at least one bridge exists.

If a terminal sits on a potential rail (e.g. PE or N), "connection top/bottom" shows only the potential name. Requirement: the net contains a free connection point or cross reference named exactly like the terminal (NUM).

In the terminal diagram every terminal strip (per location) starts on its own sheet; long strips continue on following sheets.
The terminal diagram sheets are named after their terminal strip, e.g. "Klemmenplan X1" (with a location, placed first: "Klemmenplan +1 -X1"; several sheets for one strip: "... X1 2/3"). This also applies to the table of contents and the title block.

In **Sheet properties (F2)** you also set the **sheet type** (circuit diagram, panel layout, overview, layout or custom text) and a **description**. Both appear in the table of contents; without an entry the type is "Circuit diagram" and the description stays empty.

## Importing a PDF
**File > Import PDF...** reads one page of a PDF as vector geometry (not as a picture). Choose the page and a **scale factor** (1 = paper size; enter 50 for a 1:50 plot). If the PDF contains layers (as written by AutoCAD or BricsCAD with "include layer information"), they become KatieCAD layers with the same names; layers hidden in the PDF stay hidden. Without layers everything goes onto layer "PDF". Imported: lines, polylines, rectangles, curves, circles, text and solid fills. Not imported: raster images (e.g. scanned PDFs), hatch patterns, dash line types and clipping. Text sometimes arrives in fragments. The import only uses freely licensed libraries (pypdf); KatieCAD stays MIT-licensed. To try it from source: `pip install pypdf` (also in `requirements.txt`).

## Importing an image

Note: PDF export writes KatieCAD layers as PDF layers. You can toggle them in PDF viewers and re-import such a PDF into KatieCAD with the same layer names.
**File > Import image...** inserts a photo or graphic (PNG, JPG, BMP, GIF, TIFF). The image is stored inside the drawing, so the original file is no longer needed. Resize with the yellow corner grip or **Scale**; move, rotate and mirror work as for other objects. Large images are reduced to at most 2400 pixels on the long side. Images appear in PDF output; on DXF export the image file is written next to the DXF file. Project DXF export does not include images.
