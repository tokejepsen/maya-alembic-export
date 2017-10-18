import argparse

try:
    import maya.standalone
    maya.standalone.initialize()
except RuntimeError:
    pass

from maya import cmds


def cli():
    parser = argparse.ArgumentParser(description="Alembic Exporter")

    parser.add_argument(
        "-prs", "-preRollStartFrame",
        type=float,
        action="store",
        dest="preRollStartFrame",
        default=0,
        help="The frame to start scene evaluation at.  This is used to set the"
        "starting frame for time dependent translations and can be used to "
        "evaluate run-up that isn't actually translated."
    )
    parser.add_argument(
        "-duf", "-dontSkipUnwrittenFrames",
        action="store_true",
        default=False,
        dest="dontSkipUnwrittenFrames",
        help="When evaluating multiple translate jobs, the presence of this "
        "flag decides whether to evaluate frames between jobs when there is a "
        "gap in their frame ranges."
    )
    parser.add_argument(
        "-v", "-verbose",
        action="store_true",
        default=False,
        dest="verbose",
        help="Prints the current frame that is being evaluated."
    )
    parser.add_argument(
        "-a", "-attr",
        type=str,
        action="append",
        dest="attr",
        default=[],
        help="A specific geometric attribute to write out. This flag may occur"
        " more than once."
    )
    parser.add_argument(
        "-df", "-dataFormat",
        type=str,
        action="store",
        default="Ogawa",
        dest="dataFormat",
        choices=["Ogawa", "HDF"],
        help="The data format to use to write the file.  Can be either HDF or "
        "Ogawa. The default is Ogawa."
    )
    parser.add_argument(
        "-atp", "-attrPrefix",
        type=str,
        action="append",
        default=["ABC_"],
        dest="attrPrefix",
        help="Prefix filter for determining which geometric attributes to "
        "write out. This flag may occur more than once."
    )
    parser.add_argument(
        "-ef", "-eulerFilter",
        action="store_true",
        default=False,
        dest="eulerFilter",
        help="If this flag is present, apply Euler filter while sampling "
        "rotations."
    )
    parser.add_argument(
        "-fr", "-frameRange",
        type=float,
        action="append",
        dest="frameRange",
        default=[],
        nargs=2,
        help="The frame range to write. Multiple occurrences of -frameRange "
        "are supported within a job. Each -frameRange defines a new frame "
        "range. -step or -frs will affect the current frame range only."
    )
    parser.add_argument(
        "-frs", "-frameRelativeSample",
        type=float,
        action="append",
        dest="frameRelativeSample",
        default=[],
        help="frame relative sample that will be written out along the frame "
        "range. This flag may occur more than once."
    )
    parser.add_argument(
        "-nn", "-noNormals",
        action="store_true",
        default=False,
        dest="noNormals",
        help="If this flag is present normal data for Alembic poly meshes will"
        " not be written."
    )
    parser.add_argument(
        "-pr", "-preRoll",
        action="store_true",
        default=False,
        dest="preRoll",
        help="If this flag is present, this frame range will not be sampled."
    )
    parser.add_argument(
        "-ro", "-renderableOnly",
        action="store_true",
        default=False,
        dest="renderableOnly",
        help="If this flag is present non-renderable hierarchy (invisible, or "
        "templated) will not be written out."
    )
    parser.add_argument(
        "-rt", "-root",
        action="append",
        default=[],
        dest="root",
        help="Maya dag path which will be parented to the root of the Alembic "
        "file. This flag may occur more than once.  If unspecified, it "
        "defaults to '|' which means the entire scene will be written out."
    )
    parser.add_argument(
        "-s", "-step",
        type=float,
        default=1.0,
        action="store",
        dest="step",
        help="The time interval (expressed in frames) at which the frame range"
        " is sampled. Additional samples around each frame can be specified "
        "with -frs."
    )
    parser.add_argument(
        "-sl", "-selection",
        action="store_true",
        default=False,
        dest="selection",
        help="If this flag is present, write out all all selected nodes from "
        "the active selection list that are descendents of the roots specified"
        " with -root."
    )
    parser.add_argument(
        "-sn", "-stripNamespaces",
        action="store",
        type=int,
        default=-1,
        dest="stripNamespaces",
        help="If this flag is present namespaces will be stripped off of the "
        "node before being written to Alembic. The int after the flag "
        "specifies how many namespaces will be stripped off of the node"
        " name. Be careful that the new stripped name does not collide with "
        "other sibling node names.\n\nExamples:\n taco:foo:bar would be "
        "written as just bar with -sn 0\ntaco:foo:bar would be written as "
        "foo:bar with -sn 1"
    )
    parser.add_argument(
        "-u", "-userAttr",
        type=str,
        action="append",
        dest="userAttr",
        default=[],
        help="A specific user attribute to write out.  This flag may occur "
        "more than once."
    )
    parser.add_argument(
        "-uatp", "-userAttrPrefix",
        type=str,
        action="append",
        default=[],
        dest="userAttrPrefix",
        help="Prefix filter for determining which user attributes to write "
        "out. This flag may occur more than once."
    )
    parser.add_argument(
        "-uv", "-uvWrite",
        action="store_true",
        default=False,
        dest="uvWrite",
        help="If this flag is present, uv data for PolyMesh and SubD shapes "
        "will be written to the Alembic file.  Only the current uv map is "
        "used."
    )
    parser.add_argument(
        "-wcs", "-writeColorSets",
        action="store_true",
        default=False,
        dest="writeColorSets",
        help="Write all color sets on MFnMeshes as color 3 or color 4 indexed "
        "geometry parameters with face varying scope."
    )
    parser.add_argument(
        "-wfs", "-writeFaceSets",
        action="store_true",
        default=False,
        dest="writeFaceSets",
        help="Write all Face sets on MFnMeshes."
    )
    parser.add_argument(
        "-wfg", "-wholeFrameGeo",
        action="store_true",
        default=False,
        dest="wholeFrameGeo",
        help="If this flag is present data for geometry will only be written "
        "out on whole frames."
    )
    parser.add_argument(
        "-ws", "-worldSpace",
        action="store_true",
        default=False,
        dest="worldSpace",
        help="If this flag is present, any root nodes will be stored in world "
        "space."
    )
    parser.add_argument(
        "-wv", "-writeVisibility",
        action="store_true",
        default=False,
        dest="writeVisibility",
        help="If this flag is present, visibility state will be stored in the "
        "Alembic file. Otherwise everything written out is treated as visible."
    )
    parser.add_argument(
        "-wuvs", "-writeUVSets",
        action="store_true",
        default=False,
        dest="writeUVSets",
        help="Write all uv sets on MFnMeshes as vector 2 indexed geometry"
        "parameters with face varying scope."
    )
    parser.add_argument(
        "-wc", "-writeCreases",
        action="store_true",
        default=False,
        dest="writeCreases",
        help="If this flag is present and the mesh has crease edges or crease "
        "vertices, the mesh (OPolyMesh) would now be written out as an OSubD "
        "and crease info will be stored in the Alembic file. Otherwise, "
        "creases info won't be preserved in Alembic file unless a custom "
        "Boolean attribute SubDivisionMesh has been added to mesh node and "
        "its value is true."
    )

    callback_help = """Special callback information:
    On the callbacks, special tokens are replaced with other data, these tokens
    and what they are replaced with are as follows:

    #FRAME# replaced with the frame number being evaluated.
    #FRAME# is ignored in the post callbacks.

    #BOUNDS# replaced with a string holding bounding box values in minX minY
    minZ
    maxX maxY maxZ space seperated order.

    #BOUNDSARRAY# replaced with the bounding box values as above, but in
    array form.
    In Mel: {minX, minY, minZ, maxX, maxY, maxZ}
    In Python: [minX, minY, minZ, maxX, maxY, maxZ]"""

    parser.add_argument(
        "-mfc", "-melPerFrameCallback",
        type=str,
        action="store",
        dest="melPerFrameCallback",
        help="When each frame (and the static frame) is evaluated the string "
        "specified is evaluated as a Mel command." + callback_help
    )
    parser.add_argument(
        "-mpc", "-melPostJobCallback",
        type=str,
        action="store",
        dest="melPostJobCallback",
        help="When the translation has finished the string specified is "
        "evaluated as a Mel command." + callback_help
    )
    parser.add_argument(
        "-pfc", "-pythonPerFrameCallback",
        type=str,
        action="store",
        dest="pythonPerFrameCallback",
        help="When each frame (and the static frame) is evaluated the string "
        "specified is evaluated as a python command." + callback_help
    )
    parser.add_argument(
        "-ppc", "-pythonPostJobCallback",
        type=str,
        action="store",
        dest="pythonPostJobCallback",
        help="When the translation has finished the string specified is "
        "evaluated as a python command." + callback_help
    )
    # This deviates from the direct mapping from this script to the AbcExport,
    # because we want both a Maya scene input and an Alembic file output.
    parser.add_argument(
        "-af", "-alembicFile",
        type=str,
        action="store",
        dest="alembicFile",
        required=True,
        help="File location to write the Alembic data."
    )
    parser.add_argument(
        "-mf", "-mayaFile",
        type=str,
        action="store",
        dest="mayaFile",
        required=True,
        help="File location of the Maya scene to open."
    )

    args = vars(parser.parse_args())

    mayaFile = args["mayaFile"]
    del args["mayaFile"]
    alembicFile = args["alembicFile"]
    del args["alembicFile"]

    # Opening Maya file
    cmds.file(mayaFile, open=True)

    export(alembicFile, **args)


def export(alembicFile,
           eulerFilter=False,
           noNormals=False,
           preRoll=False,
           renderableOnly=False,
           selection=False,
           uvWrite=False,
           writeColorSets=False,
           writeFaceSets=False,
           wholeFrameGeo=False,
           worldSpace=False,
           writeVisibility=False,
           writeUVSets=False,
           writeCreases=False,
           dataFormat="Ogawa",
           step=1.0,
           melPerFrameCallback="",
           melPostJobCallback="",
           pythonPerFrameCallback="",
           pythonPostJobCallback="",
           userAttr=[],
           userAttrPrefix=["ABC_"],
           attr=[],
           attrPrefix=[],
           root=[],
           frameRelativeSample=[],
           frameRange=[],
           stripNamespaces=-1,
           dontSkipUnwrittenFrames=False,
           verbose=False,
           preRollStartFrame=0
           ):
    """
    Export Alembic.

    Args:
        alembicFile (str): File location to write the Alembic data.
        eulerFilter (bool, optional): Apply Euler filter while sampling
            rotations. Defaults to False.
        noNormals (bool, optional): Present normal data for Alembic poly meshes
            will not be written. Defaults to False.
        preRoll (bool, optional): This frame range will not be sampled.
            Defaults to False.
        renderableOnly (bool, optional): Non-renderable hierarchy
            (invisible, or templated) will not be written out. Defaults to
            False.
        selection (bool, optional): Write out all all selected nodes from the
            active selection list that are descendents of the roots specified
            with -root. Defaults to False.
        uvWrite (bool, optional): Uv data for PolyMesh and SubD shapes will be
            written to the Alembic file.  Only the current uv map is used.
            Defaults to False.
        writeColorSets (bool, optional): Write all color sets on MFnMeshes as
            color 3 or color 4 indexed geometry parameters with face varying
            scope. Defaults to False.
        writeFaceSets (bool, optional): Write all Face sets on MFnMeshes.
            Defaults to False.
        wholeFrameGeo (bool, optional): Data for geometry will only be written
            out on whole frames. Defaults to False.
        worldSpace (bool, optional): Any root nodes will be stored in world
            space. Defaults to False.
        writeVisibility (bool, optional): Visibility state will be stored in
            the Alembic file.  Otherwise everything written out is treated as
            visible. Defaults to False.
        writeUVSets (bool, optional): Write all uv sets on MFnMeshes as vector
            2 indexed geometry parameters with face varying scope. Defaults to
            False.
        writeCreases (bool, optional): If the mesh has crease edges or crease
            vertices, the mesh (OPolyMesh) would now be written out as an OSubD
            and crease info will be stored in the Alembic file. Otherwise,
            creases info won't be preserved in Alembic file unless a custom
            Boolean attribute SubDivisionMesh has been added to mesh node and
            its value is true. Defaults to False.
        dataFormat (str, optional): The data format to use to write the file.
            Can be either "HDF" or "Ogawa". Defaults to "Ogawa".
        step (float, optional): The time interval (expressed in frames) at
            which the frame range is sampled. Additional samples around each
            frame can be specified with -frs. Defaults to 1.0.
        melPerFrameCallback (str, optional): When each frame
            (and the static frame) is evaluated the string specified is
            evaluated as a Mel command. See below for special processing rules.
            Defaults to "".
        melPostJobCallback (str, optional): When the translation has finished
            the string specified is evaluated as a Mel command. See below for
            special processing rules. Defaults to "".
        pythonPerFrameCallback (str, optional): When each frame
            (and the static frame) is evaluated the string specified is
            evaluated as a python command. See below for special processing
            rules. Defaults to "".
        pythonPostJobCallback (str, optional): When the translation has
            finished the string specified is evaluated as a python command. See
            below for special processing rules. Defaults to "".
        userAttrPrefix (list of str, optional): Prefix filter for determining
            which user attributes to write out. Defaults to [].
        userAttr (list of str, optional): Specific user attributes to write
            out. Defaults to [].
        attr (list of str, optional): A specific geometric attribute to write
            out. Defaults to [].
        attrPrefix (list of str, optional): Prefix filter for determining which
            geometric attributes to write out. Defaults to ["ABC_"].
        root (list of str, optional): Maya dag path which will be parented to
            the root of the Alembic file. Defaults to [], which means the
            entire scene will be written out.
        frameRelativeSample (list of float, optional): Frame relative sample
            that will be written out along the frame range. Defaults to [].
        frameRange (list of list of two floats, optional): The frame range to
            write. Each list of two floats defines a new frame range. step or
            frameRelativeSample will affect the current frame range only.
        stripNamespaces (int, optional): Namespaces will be stripped off of
            the node before being written to Alembic. The int specifies how
            many namespaces will be stripped off of the node name. Be careful
            that the new stripped name does not collide with other sibling node
            names.

            Examples:

            taco:foo:bar would be written as just bar with stripNamespaces=0
            taco:foo:bar would be written as foo:bar with stripNamespaces=1

            Defaults to -1, which means namespaces will be preserved.
        dontSkipUnwrittenFrames (bool, optional): When evaluating multiple
            translate jobs, this decides whether to evaluate frames between
            jobs when there is a gap in their frame ranges. Defaults to False.
        verbose (bool, optional): Prints the current frame that is being
            evaluated. Defaults to False.
        preRollStartFrame (float, optional): The frame to start scene
            evaluation at.  This is used to set the starting frame for time
            dependent translations and can be used to evaluate run-up that
            isn't actually translated. Defaults to 0.

    Special callback information:
    On the callbacks, special tokens are replaced with other data, these tokens
    and what they are replaced with are as follows:

    #FRAME# replaced with the frame number being evaluated.
    #FRAME# is ignored in the post callbacks.

    #BOUNDS# replaced with a string holding bounding box values in minX minY
    minZ maxX maxY maxZ space seperated order.

    #BOUNDSARRAY# replaced with the bounding box values as above, but in
    array form.
    In Mel: {minX, minY, minZ, maxX, maxY, maxZ}
    In Python: [minX, minY, minZ, maxX, maxY, maxZ]
    """

    # Generate job add_argument
    jobArg = ""

    # Boolean flags
    booleans = {
        "eulerFilter": eulerFilter,
        "noNormals": noNormals,
        "preRoll": preRoll,
        "renderableOnly": renderableOnly,
        "selection": selection,
        "uvWrite": uvWrite,
        "writeColorSets": writeColorSets,
        "writeFaceSets": writeFaceSets,
        "wholeFrameGeo": wholeFrameGeo,
        "worldSpace": worldSpace,
        "writeVisibility": writeVisibility,
        "writeUVSets": writeUVSets,
        "writeCreases": writeCreases
    }
    for key, value in booleans.iteritems():
        if value:
            jobArg += " -{0}".format(key)

    # Single argument flags
    single_arguments = {
        "dataFormat": dataFormat,
        "step": step,
        "melPerFrameCallback": melPerFrameCallback,
        "melPostJobCallback": melPostJobCallback,
        "pythonPerFrameCallback": pythonPerFrameCallback,
        "pythonPostJobCallback": pythonPostJobCallback
    }
    for key, value in single_arguments.iteritems():
        if value:
            jobArg += " -{0} \"{1}\"".format(key, value)

    # Multiple arguments flags
    multiple_arguments = {
        "attr": attr,
        "attrPrefix": attrPrefix,
        "root": root,
        "userAttrPrefix": userAttrPrefix,
        "userAttr": userAttr,
        "frameRelativeSample": frameRelativeSample
    }
    for key, value in multiple_arguments.iteritems():
        for item in value:
            jobArg += " -{0} \"{1}\"".format(key, item)

    # frame range flag
    for start, end in frameRange:
        jobArg += " -frameRange {0} {1}".format(start, end)

    # strip namespaces flag
    if stripNamespaces == 0:
        jobArg += " -stripNamespaces"
    if stripNamespaces > 0:
        jobArg += " -stripNamespaces {0}".format(stripNamespaces)

    # file flag
    # Alembic exporter does not like back slashes
    jobArg += " -file {0}".format(alembicFile.replace("\\", "/"))

    # Execute export
    cmds.loadPlugin("AbcExport.mll", quiet=True)

    export_args = {
        "dontSkipUnwrittenFrames": dontSkipUnwrittenFrames,
        "verbose": verbose,
        "preRollStartFrame": preRollStartFrame,
        "jobArg": jobArg
    }

    print("Exporting with: {0}".format(export_args))

    cmds.AbcExport(**export_args)


if __name__ == "__main__":
    cli()
